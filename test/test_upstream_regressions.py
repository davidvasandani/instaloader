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

    def test_csrf_network_failures_use_instaloader_exception(self):
        for failure in (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            with self.subTest(failure=failure), closing(InstaloaderContext(sleep=False, quiet=True)) as context:
                with patch.object(context._session, 'get', side_effect=failure('offline')):
                    with self.assertRaises(ConnectionException) as raised:
                        context.doc_id_graphql_query('123', {})
                self.assertIsInstance(raised.exception.__cause__, failure)


if __name__ == '__main__':
    unittest.main()
