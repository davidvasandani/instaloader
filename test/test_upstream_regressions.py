"""Offline regression tests for issues identified during upstream sync review."""
from contextlib import closing
import unittest
from unittest.mock import Mock, patch

import requests
from instaloader import (AbortDownloadException, ConnectionException, InstaloaderContext,
                        LoginRequiredException, Post, QueryReturnedBadRequestException)


class UpstreamRegressionTests(unittest.TestCase):
    def test_existing_play_count_is_preserved_without_another_request(self):
        for count in (0, 42):
            with self.subTest(count=count):
                context = Mock()
                media = {'media_type': 2, 'code': 'ABC', 'pk': '123',
                         'taken_at': 1, 'user': {'pk': '1'}, 'play_count': count}
                normalized = Post._normalize_post_data(media, context)
                self.assertEqual(normalized['video_play_count'], count)
                context.doc_id_graphql_query.assert_not_called()

    def test_missing_play_count_uses_fallback(self):
        context = Mock()
        context.doc_id_graphql_query.return_value = {'data': {
            'xdt_api__v1__clips__user__connection_v2': {
                'edges': [{'node': {'media': {'code': 'ABC', 'play_count': 42}}}]}}}
        media = {'media_type': 2, 'code': 'ABC', 'pk': '123',
                 'taken_at': 1, 'user': {'pk': '1'}}
        self.assertEqual(Post._normalize_post_data(media, context)['video_play_count'], 42)
        context.doc_id_graphql_query.assert_called_once()

    def test_location_identifiers_are_compatible_with_geotags(self):
        for identifier in ({'pk': '456'}, {'id': '456'}, {'id': '456', 'pk': '789'}):
            with self.subTest(identifier=identifier):
                context = Mock()
                context.is_logged_in = True
                location = dict(identifier, name='Place', slug='place', has_public_page=True,
                                lat=1.0, lng=2.0)
                media = {'media_type': 1, 'code': 'ABC', 'pk': '123', 'taken_at': 1,
                         'user': {'pk': '1', 'username': 'owner'}, 'location': location}
                context.doc_id_graphql_query.return_value = {'data': {
                    'xdt_api__v1__media__shortcode__web_info': {'items': [media]}}}
                post = Post.from_shortcode(context, 'ABC')
                self.assertEqual(post.location.id, 456)
                self.assertEqual((post.location.lat, post.location.lng), (1.0, 2.0))
                self.assertEqual(set(location).intersection({'id', 'pk'}), set(identifier))
                context.get_json.assert_not_called()

    def test_liker_ids_and_hashing_do_not_fetch_profile_metadata(self):
        context = Mock()
        context.is_logged_in = True
        users = [{'pk': '42', 'username': 'one'}, {'id': '43', 'username': 'two'}]
        context.get_json.return_value = {'users': users}
        post = Post(context, {'shortcode': 'ABC', 'id': '123',
                              'edge_media_preview_like': {'count': 2}})
        profiles = set(post.get_likes())
        self.assertEqual({profile.userid for profile in profiles}, {42, 43})
        context.get_json.assert_called_once_with('api/v1/media/123/likers/', {})
        context.doc_id_graphql_query.assert_not_called()
        self.assertNotIn('id', users[0])

    def test_page_and_csrf_requests_honor_fatal_status_codes(self):
        for status in (302, 404, 429):
            with self.subTest(status=status), closing(InstaloaderContext(
                    sleep=False, quiet=True, fatal_status_codes=[status])) as context:
                response = requests.Response()
                response.status_code = status
                response.reason = 'test response'
                response._content = b''
                with patch('requests.sessions.Session.request', return_value=response), \
                        patch.object(context._rate_controller, 'wait_before_query'), \
                    patch.object(context._rate_controller, 'handle_429'):
                    with self.assertRaises(AbortDownloadException):
                        context.get_page_data('example/')
                    context._session.cookies.clear()
                    with patch.object(context._session, 'get', return_value=response), \
                            self.assertRaises(AbortDownloadException):
                        context.doc_id_graphql_query('123', {})

    def test_page_nonfatal_failure_is_recoverable(self):
        with closing(InstaloaderContext(sleep=False, quiet=True)) as context:
            response = requests.Response()
            response.status_code = 429
            response.reason = 'Too Many Requests'
            response._content = b''
            with patch('requests.sessions.Session.request', return_value=response), \
                    patch.object(context._rate_controller, 'wait_before_query'), \
                    patch.object(context._rate_controller, 'handle_429'):
                with self.assertRaises(ConnectionException):
                    context.get_page_data('example/')

    def test_missing_web_video_url_uses_iphone_candidate(self):
        for web_versions in (None, []):
            with self.subTest(web_versions=web_versions):
                context = Mock()
                context.is_logged_in = True
                context.iphone_support = True
                media = {'media_type': 2, 'code': 'ABC', 'pk': '123', 'taken_at': 1,
                         'user': {'pk': '1'}, 'play_count': 1, 'video_versions': web_versions}
                context.doc_id_graphql_query.return_value = {'data': {
                    'xdt_api__v1__media__shortcode__web_info': {'items': [media]}}}
                context.get_iphone_json.return_value = {'items': [
                    {'video_versions': [{'url': 'https://example.com/video.mp4'}]}]}
                post = Post.from_shortcode(context, 'ABC')
                self.assertEqual(post.video_url, 'https://example.com/video.mp4')
                context.head.assert_not_called()
                context.iphone_support = False
                self.assertIsNone(post.video_url)

    def test_carousel_video_uses_iphone_fallback(self):
        for versions in (None, []):
            with self.subTest(versions=versions):
                context = Mock()
                context.is_logged_in = True
                context.iphone_support = True
                child = {'media_type': 2, 'video_versions': versions,
                         'image_versions2': {'candidates': [{'url': 'https://example.com/thumb.jpg'}]}}
                media = {'media_type': 8, 'code': 'ABC', 'pk': '123', 'taken_at': 1,
                         'user': {'pk': '1'}, 'carousel_media': [child]}
                context.doc_id_graphql_query.return_value = {'data': {
                    'xdt_api__v1__media__shortcode__web_info': {'items': [media]}}}
                context.get_iphone_json.return_value = {'items': [{'carousel_media': [
                    {'video_versions': [{'url': 'https://example.com/video.mp4'}]}]}]}
                post = Post.from_shortcode(context, 'ABC')
                self.assertEqual(list(post.get_sidecar_nodes())[0].video_url, 'https://example.com/video.mp4')
                context.get_iphone_json.assert_called_once()
                context.iphone_support = False
                self.assertIsNone(list(post.get_sidecar_nodes())[0].video_url)

    @staticmethod
    def response(status):
        response = requests.Response()
        response.status_code = status
        response.reason = 'test response'
        response._content = b'<script type="application/json">{"__bbox":{"result":{"data":{"ok":true}}}}</script>'
        return response

    def test_page_retries_transient_failures_and_backs_off_on_429(self):
        for failure in (requests.exceptions.Timeout('offline'), self.response(503), self.response(429)):
            with self.subTest(failure=failure), closing(InstaloaderContext(
                    sleep=False, quiet=True, max_connection_attempts=3)) as context:
                with patch('requests.sessions.Session.request', side_effect=[failure, self.response(200)]) as request, \
                        patch.object(context._rate_controller, 'wait_before_query'), \
                        patch.object(context._rate_controller, 'handle_429') as backoff, \
                        patch.object(context, 'error'):
                    self.assertEqual(context.get_page_data('example/'), [{'ok': True}])
                self.assertEqual(request.call_count, 2)
                if isinstance(failure, requests.Response) and failure.status_code == 429:
                    backoff.assert_called_once_with('other')
                else:
                    backoff.assert_not_called()

    def test_page_retry_limit_and_unlimited_retry_setting(self):
        for limit in (0, 2):
            with self.subTest(limit=limit), closing(InstaloaderContext(
                    sleep=False, quiet=True, max_connection_attempts=limit)) as context:
                with patch('requests.sessions.Session.request',
                           side_effect=[self.response(503), self.response(503), self.response(200)]) as request, \
                        patch.object(context._rate_controller, 'wait_before_query'), \
                        patch.object(context, 'error'):
                    if limit:
                        with self.assertRaises(ConnectionException):
                            context.get_page_data('example/')
                        self.assertEqual(request.call_count, 2)
                    else:
                        self.assertEqual(context.get_page_data('example/'), [{'ok': True}])
                        self.assertEqual(request.call_count, 3)

    def test_optional_play_count_failures_do_not_block_usable_media(self):
        media = {'media_type': 2, 'code': 'ABC', 'pk': '123', 'taken_at': 1,
                 'user': {'pk': '1'}, 'video_versions': [{'url': 'https://example.com/video.mp4'}]}
        for error in (QueryReturnedBadRequestException, LoginRequiredException, ConnectionException):
            with self.subTest(error=error):
                context = Mock()
                context.doc_id_graphql_query.side_effect = error('unavailable')
                normalized = Post._normalize_post_data(media, context)
                self.assertIsNone(normalized['video_play_count'])
                self.assertEqual(normalized['video_url'], 'https://example.com/video.mp4')
        context.doc_id_graphql_query.side_effect = AbortDownloadException('explicit abort')
        with self.assertRaises(AbortDownloadException):
            Post._normalize_post_data(media, context)

    def test_retry_interrupt_is_recoverable_but_first_attempt_interrupt_is_not(self):
        for retry in (False, True):
            with self.subTest(retry=retry), closing(InstaloaderContext(sleep=False, quiet=True)) as context:
                effects = ([self.response(503)] if retry else []) + [KeyboardInterrupt()]
                with patch('requests.sessions.Session.request', side_effect=effects), \
                        patch.object(context._rate_controller, 'wait_before_query'), \
                        patch.object(context, 'error'):
                    with self.assertRaises(ConnectionException if retry else KeyboardInterrupt):
                        context.get_page_data('example/')

    def test_caption_normalization_handles_absent_and_present_text(self):
        for caption, expected in ((None, None), ({}, None), ({'text': None}, None),
                                  ({'text': ''}, ''), ({'text': '#hello @world'}, '#hello @world'),
                                  ('legacy text', 'legacy text')):
            with self.subTest(caption=caption):
                context = Mock()
                media = {'media_type': 1, 'code': 'ABC', 'pk': '123', 'taken_at': 1,
                         'user': {'pk': '1'}, 'caption': caption}
                context.doc_id_graphql_query.return_value = {'data': {
                    'xdt_api__v1__media__shortcode__web_info': {'items': [media]}}}
                post = Post.from_shortcode(context, 'ABC')
                self.assertEqual(post.caption, expected)
                self.assertEqual(post.caption_hashtags, ['hello'] if expected == '#hello @world' else [])
                self.assertEqual(post.caption_mentions, ['world'] if expected == '#hello @world' else [])
                self.assertEqual(media['caption'], caption)

    def test_csrf_network_failures_use_instaloader_exception(self):
        for failure in (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            with self.subTest(failure=failure), closing(InstaloaderContext(sleep=False, quiet=True)) as context:
                with patch.object(context._session, 'get', side_effect=failure('offline')):
                    with self.assertRaises(ConnectionException) as raised:
                        context.doc_id_graphql_query('123', {})
                self.assertIsInstance(raised.exception.__cause__, failure)


if __name__ == '__main__':
    unittest.main()
