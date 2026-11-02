
from flask import Blueprint

products = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    url_prefix="/products"
)

from app.products import views
