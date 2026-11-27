"""Offline coverage of public profile pagination and recoverable missing posts."""
import unittest
from contextlib import closing
from unittest.mock import patch

from instaloader import ConnectionException, InstaloaderContext, Post, Profile, QueryReturnedNotFoundException


class PublicTimelineTests(unittest.TestCase):
    def test_missing_post_does_not_prevent_pagination(self):
        first_page = {
            'edges': [{'node': {'code': 'gone'}}],
            'page_info': {'has_next_page': True, 'end_cursor': 'next'},
        }
        second_page = {'edges': [{'node': {'code': 'kept'}}]}
        with closing(InstaloaderContext(sleep=False, quiet=True)) as context:
            profile = Profile(context, {'username': 'example', 'id': '1'})
            kept = Post(context, {'shortcode': 'kept'})
            with patch.object(context, 'get_page_data', return_value=[
                {'xig_user_by_username': {'id': 'page-id', 'polaris_ordered_timeline_connection': first_page}}
            ]), patch.object(context, 'doc_id_graphql_query', return_value={
                'data': {'node': {'polaris_ordered_timeline_connection': second_page}}
            }) as query, patch.object(Post, 'from_shortcode', side_effect=[
                QueryReturnedNotFoundException('gone'), kept,
            ]):
                self.assertEqual(list(profile.get_posts()), [kept])
                self.assertEqual(query.call_args.args[1]['after'], 'next')
                self.assertTrue(query.call_args.args[3])

    def test_throttle_stops_iteration(self):
        with closing(InstaloaderContext(sleep=False, quiet=True)) as context:
            profile = Profile(context, {'username': 'example', 'id': '1'})
            page = {'edges': [{'node': {'code': 'post'}}]}
            with patch.object(context, 'get_page_data', return_value=[
                {'xig_user_by_username': {'id': 'page-id', 'polaris_ordered_timeline_connection': page}}
            ]), patch.object(Post, 'from_shortcode', side_effect=ConnectionException('throttled')):
                with self.assertRaisesRegex(ConnectionException, 'throttled'):
                    next(profile.get_posts())
