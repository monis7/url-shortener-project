# tests/test_url_shortener.py

import unittest
from service.url_service import generate_short_url, ensure_unique_short_url

class TestUrlShortener(unittest.TestCase):

    def test_generate_short_url(self):
        short_url = generate_short_url(6)
        self.assertIsNotNone(short_url)
        self.assertEqual(len(short_url), 6)

    def test_generate_short_url_uniqueness(self):
        existing_urls = {"abcdef"}
        short_url = ensure_unique_short_url(existing_urls, 6)
        self.assertNotIn(short_url, existing_urls)

    def test_generate_short_url_custom_length(self):
        custom_length = 10
        short_url = generate_short_url(custom_length)
        self.assertEqual(len(short_url), custom_length)

    def test_generate_short_url_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_short_url(0)

    def test_generate_short_url_negative_length(self):
        with self.assertRaises(ValueError):
            generate_short_url(-5)

if __name__ == '__main__':
    unittest.main()
