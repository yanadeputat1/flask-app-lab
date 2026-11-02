
from flask import render_template, abort
from app.products import products


products_list = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 1200,
        "content": "Ноутбук для навчання та роботи."
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 800,
        "content": "Смартфон із OLED-дисплеєм та подвійною камерою."
    },
    {
        "id": 3,
        "name": "PC",
        "price": 1800,
        "content": "Настільний комп'ютер для ігор і роботи."
    }
]


@products.route("/")
def list_products():
    return render_template(
        "products/products.html",
        title="Наші товари",
        products=products_list
    )


@products.route("/<int:product_id>")
def detail_product(product_id):
    product = next(
        (p for p in products_list if p["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product
    )
