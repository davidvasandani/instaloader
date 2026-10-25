"""Offline regression coverage for the fork's URL enumeration extension."""
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from instaloader import Instaloader, LoginRequiredException
from instaloader.__main__ import ExitCode, _main


class ListOnlyTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        previous = os.getcwd()
        os.chdir(self.directory.name)
        self.addCleanup(os.chdir, previous)
        self.loader = Instaloader(quiet=True)
        self.addCleanup(self.loader.close)
        # Any unexpected network request or download fails the test.
        self.network = patch('requests.sessions.Session.request',
                             side_effect=AssertionError('Unexpected network request')).start()
        self.addCleanup(patch.stopall)
        self.download = patch.object(self.loader, 'download_post',
                                     side_effect=AssertionError('Unexpected download')).start()

    @staticmethod
    def posts():
        return iter(SimpleNamespace(shortcode=code) for code in ('one', 'two', 'three'))

    def test_filter_and_limit_export_only_matching_urls(self):
        self.loader.list_posts_to_file(self.posts(), '#example', max_count=1,
                                       post_filter=lambda post: post.shortcode != 'one')
        self.assertEqual(Path('hashtag_example_urls.txt').read_text(),
                         'https://www.instagram.com/p/two/\n')
        self.download.assert_not_called()

    def test_explicit_filename_and_empty_result(self):
        self.loader.list_posts_to_file(iter(()), ':saved', filename='custom.txt')
        self.assertEqual(Path('custom.txt').read_text(), '')

    def test_saved_posts_require_login(self):
        with self.assertRaises(LoginRequiredException):
            self.loader.list_saved_posts()

    def test_saved_posts_export(self):
        self.loader.context.username = 'owner'
        profile = Mock()
        profile.get_saved_posts.return_value = self.posts()
        with patch('instaloader.instaloader.Profile.own_profile', return_value=profile):
            self.loader.list_saved_posts(max_count=2)
        self.assertEqual(Path('saved_urls.txt').read_text().splitlines(), [
            'https://www.instagram.com/p/one/', 'https://www.instagram.com/p/two/'])

    def test_profile_list_mode_and_normal_mode(self):
        profile = Mock()
        profile.username = 'example'
        profile.get_posts.return_value = self.posts()
        with patch.object(self.loader, 'check_profile_id', return_value=profile), \
                patch.object(self.loader, 'download_profiles') as download_profiles:
            result = _main(self.loader, ['example'], list_only=True)
            self.assertEqual(result, ExitCode.SUCCESS)
            download_profiles.assert_not_called()
            self.assertEqual(len(Path('example_urls.txt').read_text().splitlines()), 3)
            _main(self.loader, ['example'], list_only=False)
            download_profiles.assert_called_once()

    def test_saved_cli_routes_to_listing(self):
        with patch.object(self.loader, 'list_saved_posts') as listing, \
                patch.object(self.loader, 'download_saved_posts') as downloading:
            self.assertEqual(_main(self.loader, [':saved'], list_only=True, max_count=2),
                             ExitCode.SUCCESS)
            listing.assert_called_once_with(max_count=2, post_filter=None, filename='saved_urls.txt')
            downloading.assert_not_called()

    def test_feed_and_hashtag_routes_export_urls(self):
        hashtag = Mock()
        hashtag.get_posts_resumable.return_value = self.posts()
        with patch.object(self.loader, 'get_feed_posts', return_value=self.posts()), \
                patch('instaloader.structures.Hashtag.from_name', return_value=hashtag), \
                patch.object(self.loader, 'download_feed_posts') as feed_download, \
                patch.object(self.loader, 'download_hashtag') as hashtag_download:
            self.assertEqual(_main(self.loader, [':feed', '#example'], list_only=True),
                             ExitCode.SUCCESS)
            feed_download.assert_not_called()
            hashtag_download.assert_not_called()
        self.assertEqual(Path('feed_urls.txt').read_text(), Path('hashtag_example_urls.txt').read_text())


if __name__ == '__main__':
    unittest.main()
