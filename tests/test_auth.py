import unittest

from app import create_app
from app.extensions import db
from app.users.models import User


class FlaskLoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app.config["WTF_CSRF_ENABLED"] = False

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()

        # Створення тестового користувача
        user = User(
            username="testuser",
            email="testuser@example.com"
        )
        user.set_password("password123")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_page(self):
        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/users/login")

        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "password123"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testuser", response.data)

    def test_wrong_password(self):
        response = self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "wrongpassword"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Неправильний логін або пароль.".encode("utf-8"),
            response.data
        )

    def test_successful_registration(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(username="newuser").first()

        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("password123"))
        self.assertIn(b"newuser", response.data)

    def test_logout(self):
        self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )

        response = self.client.get(
            "/users/logout",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Ви вийшли з акаунта.".encode("utf-8"),
            response.data
        )

    def test_profile_requires_login(self):
        response = self.client.get("/users/profile")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.location)


if __name__ == "__main__":
    unittest.main()
