# tests/test_integration.py

import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestIntegration(unittest.TestCase):

    def test_shorten_url(self):
        response = client.post("/shorten_url", json={"url": "https://example.com"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("short_url", data)
        self.assertIn("original_url", data)
        self.assertEqual(data["original_url"], "https://example.com")

    def test_shorten_url_with_custom_short_url(self):
        response = client.post("/shorten_url", json={"url": "https://example.com", "short_url": "custom123"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["short_url"], "custom123")
        self.assertEqual(data["original_url"], "https://example.com")

    def test_redirect_url(self):
        client.post("/shorten_url", json={"url": "https://example.com", "short_url": "test123"})
        response = client.get("/redirect/test123")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["original_url"], "https://example.com")

    def test_redirect_invalid_short_url(self):
        response = client.get("/redirect/invalid123")
        self.assertEqual(response.status_code, 404)

    def test_list_urls(self):
        client.post("/shorten_url", json={"url": "https://example.com", "short_url": "listtest"})
        response = client.get("/list_urls")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(any(item["short_url"] == "listtest" for item in data))

    def test_invalid_url_format(self):
        response = client.post("/shorten_url", json={"url": "invalid-url"})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
