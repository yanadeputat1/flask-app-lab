import unittest

from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Привіт, John!".encode("utf-8"), response.data)
        self.assertIn("30".encode("utf-8"), response.data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Адміністратор".encode("utf-8"), response.data)
        self.assertIn("Мій профіль".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
