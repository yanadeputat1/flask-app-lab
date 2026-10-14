
from flask import Flask

app = Flask(__name__)

from app import views
from app.users import users
from app.products import products

app.register_blueprint(users)
app.register_blueprint(products)
