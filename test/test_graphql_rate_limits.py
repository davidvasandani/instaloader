"""HTTP-200 GraphQL throttling must follow the existing retry policy."""
import unittest
from contextlib import closing
from unittest.mock import Mock, call

from instaloader import AbortDownloadException, ConnectionException, InstaloaderContext


THROTTLE = {'errors': [{'message': 'Rate limit exceeded', 'severity': 'CRITICAL', 'code': 1675004}]}


def response(payload, status=200):
    result = Mock(status_code=status, is_redirect=False, headers={'Content-Type': 'application/json'},
                  reason='Too Many Requests' if status == 429 else 'OK',
                  url='https://www.instagram.com/graphql/query', text='{}')
    result.json.return_value = payload
    return result


class GraphQLRateLimitTests(unittest.TestCase):
    def context(self, attempts=3, fatal=None):
        context = InstaloaderContext(sleep=False, quiet=True, max_connection_attempts=attempts,
                                    fatal_status_codes=fatal)
        context._rate_controller = Mock()
        context.error = Mock()
        return context

    def test_throttle_then_success_preserves_method_body_and_headers(self):
        for use_post in (True, False):
            for query_key in ('doc_id', 'query_hash'):
                with self.subTest(post=use_post, key=query_key), closing(self.context()) as context:
                    session = Mock()
                    method = session.post if use_post else session.get
                    success = {'data': {'items': [{'id': '123'}]}}
                    method.side_effect = [response(THROTTLE), response(success)]
                    params = {query_key: '123', 'variables': '{"shortcode":"ABC"}'}
                    headers = {}
                    self.assertEqual(context.get_json('graphql/query', params, session=session,
                                                      use_post=use_post, response_headers=headers), success)
                    argument = {'data' if use_post else 'params': params}
                    self.assertEqual(method.call_args_list, [call(
                        'https://www.instagram.com/graphql/query', allow_redirects=False, **argument)] * 2)
                    (session.get if use_post else session.post).assert_not_called()
                    context._rate_controller.handle_429.assert_called_once_with('123')
                    self.assertEqual(headers['Content-Type'], 'application/json')

    def test_exhaustion_is_bounded_and_reports_rate_limit(self):
        for attempts in (1, 3):
            with self.subTest(attempts=attempts), closing(self.context(attempts)) as context:
                session = Mock()
                session.post.return_value = response(THROTTLE)
                with self.assertRaisesRegex(ConnectionException, 'GraphQL rate limit exceeded'):
                    context.get_json('graphql/query', {'doc_id': '123'}, session=session, use_post=True)
                self.assertEqual(session.post.call_count, attempts)
                self.assertEqual(context._rate_controller.handle_429.call_count, attempts - 1)
                session.get.assert_not_called()

    def test_unrelated_errors_and_non_graphql_responses_are_unchanged(self):
        payloads = [{'data': {}}, {'errors': None}, {'errors': {}}, {'errors': 'invalid'},
                    {'errors': [None, 'invalid', {'code': 42}, {'message': 'Rate limit exceeded'}]}]
        for payload in payloads:
            with self.subTest(payload=payload), closing(self.context()) as context:
                session = Mock()
                session.post.return_value = response(payload)
                self.assertEqual(context.get_json('graphql/query', {'doc_id': '123'},
                                                  session=session, use_post=True), payload)
                context._rate_controller.handle_429.assert_not_called()
        with closing(self.context()) as context:
            session = Mock()
            session.get.return_value = response(THROTTLE)
            self.assertEqual(context.get_json('api/v1/test/', {}, session=session), THROTTLE)
            context._rate_controller.handle_429.assert_not_called()

    def test_http_429_retry_preserves_post_and_fatal_policy(self):
        with closing(self.context()) as context:
            session = Mock()
            session.post.side_effect = [response({}, 429), response({'data': {}})]
            self.assertEqual(context.get_json('graphql/query', {'doc_id': '123'},
                                              session=session, use_post=True), {'data': {}})
            self.assertEqual(session.post.call_count, 2)
            session.get.assert_not_called()
            context._rate_controller.handle_429.assert_called_once_with('123')
        with closing(self.context(fatal=[429])) as context:
            session = Mock()
            session.post.return_value = response({}, 429)
            with self.assertRaises(AbortDownloadException):
                context.get_json('graphql/query', {'doc_id': '123'}, session=session, use_post=True)
            context._rate_controller.handle_429.assert_not_called()
            self.assertEqual(session.post.call_count, 1)


if __name__ == '__main__':
    unittest.main()
