import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app as minehosting


class MineHostingAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = minehosting.DATABASE_PATH
        minehosting.DATABASE_PATH = Path(self.temp_dir.name) / "status.db"
        self.environ = patch.dict(
            os.environ,
            {"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "test-password"},
        )
        self.environ.start()
        minehosting.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = minehosting.app.test_client()

    def tearDown(self):
        self.environ.stop()
        minehosting.DATABASE_PATH = self.database_path
        self.temp_dir.cleanup()

    def csrf_token(self, response):
        match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
        self.assertIsNotNone(match)
        return match.group(1).decode()

    def sign_in(self):
        response = self.client.get("/admin/login")
        return self.client.post(
            "/admin/login",
            data={
                "csrf_token": self.csrf_token(response),
                "username": "admin",
                "password": "test-password",
            },
            follow_redirects=True,
        )

    def test_public_pages_render(self):
        self.assertIn(b"MINE", self.client.get("/").data)
        self.assertIn(b"System status", self.client.get("/status").data)

    def test_admin_can_add_service_and_csrf_is_required(self):
        self.assertEqual(self.client.get("/admin").status_code, 302)
        self.sign_in()
        response = self.client.post(
            "/admin/sites/add",
            data={"name": "Main site", "url": "https://example.com"},
        )
        self.assertEqual(response.status_code, 400)

        dashboard = self.client.get("/admin")
        response = self.client.post(
            "/admin/sites/add",
            data={
                "csrf_token": self.csrf_token(dashboard),
                "name": "Main site",
                "url": "https://example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(b"Main site", self.client.get("/admin").data)

    def test_private_and_nonstandard_targets_are_rejected(self):
        for url in (
            "http://127.0.0.1/",
            "http://192.168.1.1/",
            "http://localhost/",
            "https://example.com:8443/",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                minehosting.validate_site_url(url)

        self.assertEqual(
            minehosting.validate_site_url("https://example.com"),
            "https://example.com/",
        )

    def test_dns_results_are_rechecked_before_connecting(self):
        with patch("app.resolve_public_addresses", return_value=[]):
            self.assertEqual(
                minehosting.check_site("https://example.com/"),
                ("down", None, None),
            )


if __name__ == "__main__":
    unittest.main()
