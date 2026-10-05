import os
import tempfile
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_public_homepage_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("LIQUOR SHOP", response.get_data(as_text=True).upper())

    def test_admin_login_and_dashboard(self):
        response = self.client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dashboard", response.get_data(as_text=True))

    def test_import_preview_parses_csv(self):
        self.client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=True,
        )

        csv_text = "product_name,brand,category,size,price\nBlue Moon,Blue Moon,Whisky,750ml,2500\nBlue Moon,Blue Moon,Whisky,375ml,1300\n"
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as handle:
            handle.write(csv_text)
            temp_path = handle.name

        with open(temp_path, "rb") as handle:
            response = self.client.post(
                "/admin/import",
                data={"file": (handle, "sample.csv")},
                content_type="multipart/form-data",
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("Imported", response.get_data(as_text=True))

        os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
