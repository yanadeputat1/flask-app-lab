
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory
)
from werkzeug.utils import secure_filename
from tinydb import TinyDB

from app.products import products
from app.forms import ProductForm


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "products.json"

UPLOAD_FOLDER = Path(__file__).resolve().parent / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


def prepare_database():
    """Створює базу TinyDB та переносить старі дані, якщо потрібно."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if DATA_FILE.exists():
        try:
            old_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            old_data = {}

        # Перенесення даних зі старого JSON-списку до TinyDB.
        if isinstance(old_data, list):
            DATA_FILE.unlink()

            with TinyDB(str(DATA_FILE)) as db:
                if old_data:
                    db.insert_multiple(old_data)

    with TinyDB(str(DATA_FILE)):
        pass


def load_products():
    """Завантажує товари з TinyDB."""
    prepare_database()

    with TinyDB(str(DATA_FILE)) as db:
        return db.all()


def save_products(products_list):
    """Зберігає товари в TinyDB."""
    prepare_database()

    with TinyDB(str(DATA_FILE)) as db:
        db.truncate()
        if products_list:
            db.insert_multiple(products_list)


def allowed_file(filename):
    """Перевіряє формат зображення."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_product_image(file):
    """Перевіряє та зберігає зображення товару."""
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename):
        raise ValueError(
            "Дозволені лише зображення PNG, JPG та JPEG."
        )

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_IMAGE_SIZE:
        raise ValueError(
            "Розмір зображення не повинен перевищувати 5 МБ."
        )

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    original_name = secure_filename(file.filename)
    extension = original_name.rsplit(".", 1)[1].lower()
    filename = f"{uuid4().hex}.{extension}"

    file.save(UPLOAD_FOLDER / filename)

    return f"uploads/{filename}"


def delete_product_image(image_path):
    """Видаляє зображення товару."""
    if not image_path or not image_path.startswith("uploads/"):
        return

    image_file = (UPLOAD_FOLDER / Path(image_path).name).resolve()

    if image_file.parent == UPLOAD_FOLDER.resolve() and image_file.exists():
        image_file.unlink()


@products.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(str(UPLOAD_FOLDER), filename)


@products.route("/")
def list_products():
    return render_template(
        "products/products.html",
        title="Наші товари",
        products=load_products()
    )


@products.route("/<int:product_id>")
def detail_product(product_id):
    product = next(
        (p for p in load_products() if p["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product
    )


@products.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        products_list = load_products()

        try:
            image_path = save_product_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "products/add_product.html",
                title="Додати товар",
                form=form
            )

        product_id = max(
            (p["id"] for p in products_list),
            default=0
        ) + 1

        new_product = {
            "id": product_id,
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path or "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        products_list.append(new_product)
        save_products(products_list)

        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.list_products"))

    return render_template(
        "products/add_product.html",
        title="Додати товар",
        form=form
    )


@products.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    products_list = load_products()

    product = next(
        (p for p in products_list if p["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        try:
            new_image_path = save_product_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "products/edit_product.html",
                title="Редагувати товар",
                form=form,
                product=product
            )

        product["name"] = form.name.data
        product["content"] = form.content.data
        product["price"] = float(form.price.data)
        product["category"] = form.category.data
        product["quantity"] = form.quantity.data

        if new_image_path:
            old_image_path = product.get("image", "")
            product["image"] = new_image_path
            delete_product_image(old_image_path)

        save_products(products_list)

        flash("Товар успішно відредаговано!", "success")
        return redirect(url_for("products.list_products"))

    if request.method == "GET":
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = product["price"]
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    return render_template(
        "products/edit_product.html",
        title="Редагувати товар",
        form=form,
        product=product
    )


@products.route("/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    products_list = load_products()

    product = next(
        (p for p in products_list if p["id"] == product_id),
        None
    )

    if product is None:
        abort(404)

    delete_product_image(product.get("image", ""))

    products_list = [
        p for p in products_list
        if p["id"] != product_id
    ]

    save_products(products_list)

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.list_products"))
