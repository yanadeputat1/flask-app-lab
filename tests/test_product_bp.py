
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from app import app
from app.products.views import load_products


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_products_page(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_second_product_detail(self):
        response = self.client.get("/products/2")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)

    def test_add_product(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "products.json"

            with patch("app.products.views.DATA_FILE", test_file):
                response = self.client.post(
                    "/products/add",
                    data={
                        "name": "Test Laptop",
                        "content": "Тестовий опис товару",
                        "price": "1500.00",
                        "category": "Електроніка",
                        "quantity": "5",
                    },
                    follow_redirects=True
                )

                self.assertEqual(response.status_code, 200)

                saved_products = load_products()
                self.assertEqual(len(saved_products), 1)
                self.assertEqual(saved_products[0]["name"], "Test Laptop")

    def test_edit_product(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "products.json"

            with patch("app.products.views.DATA_FILE", test_file):
                self.client.post(
                    "/products/add",
                    data={
                        "name": "Old Product",
                        "content": "Старий опис",
                        "price": "100.00",
                        "category": "Книги",
                        "quantity": "2",
                    },
                    follow_redirects=True
                )

                product_id = load_products()[0]["id"]

                response = self.client.post(
                    f"/products/{product_id}/edit",
                    data={
                        "name": "New Product",
                        "content": "Новий опис",
                        "price": "200.00",
                        "category": "Книги",
                        "quantity": "4",
                    },
                    follow_redirects=True
                )

                self.assertEqual(response.status_code, 200)

                saved_products = load_products()
                self.assertEqual(saved_products[0]["name"], "New Product")
                self.assertEqual(saved_products[0]["quantity"], 4)

    def test_delete_product(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "products.json"

            with patch("app.products.views.DATA_FILE", test_file):
                self.client.post(
                    "/products/add",
                    data={
                        "name": "Delete Product",
                        "content": "Товар для видалення",
                        "price": "50.00",
                        "category": "Інше",
                        "quantity": "1",
                    },
                    follow_redirects=True
                )

                product_id = load_products()[0]["id"]

                response = self.client.post(
                    f"/products/{product_id}/delete",
                    follow_redirects=True
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(load_products(), [])


if __name__ == "__main__":
    unittest.main()
