"""Offline regression tests for issues identified during upstream sync review."""
from contextlib import closing
import unittest
from unittest.mock import Mock, patch

import requests
from instaloader import ConnectionException, InstaloaderContext, Post


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

    def test_csrf_network_failures_use_instaloader_exception(self):
        for failure in (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            with self.subTest(failure=failure), closing(InstaloaderContext(sleep=False, quiet=True)) as context:
                with patch.object(context._session, 'get', side_effect=failure('offline')):
                    with self.assertRaises(ConnectionException) as raised:
                        context.doc_id_graphql_query('123', {})
                self.assertIsInstance(raised.exception.__cause__, failure)


if __name__ == '__main__':
    unittest.main()
