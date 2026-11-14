"""Insert data into products table

Revision ID: fdfc1d3ab1f0
Revises: 4b75daaa291d
Create Date: 2026-11-13 14:52:59.456271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdfc1d3ab1f0'
down_revision = '4b75daaa291d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text(
        "INSERT INTO categories (name) "
        "SELECT 'Laptops' "
        "WHERE NOT EXISTS "
        "(SELECT 1 FROM categories WHERE name = 'Laptops')"
    ))

    op.execute(sa.text(
        "INSERT INTO products "
        "(name, price, category_id, active, created_at) "
        "SELECT 'iPhone 15', 999.99, NULL, 1, CURRENT_TIMESTAMP "
        "WHERE NOT EXISTS "
        "(SELECT 1 FROM products WHERE name = 'iPhone 15')"
    ))

    op.execute(sa.text(
        "INSERT INTO products "
        "(name, price, category_id, active, created_at) "
        "SELECT 'Gaming Laptop', 1500.00, id, 0, CURRENT_TIMESTAMP "
        "FROM categories "
        "WHERE name = 'Laptops' "
        "AND NOT EXISTS "
        "(SELECT 1 FROM products WHERE name = 'Gaming Laptop')"
    ))


def downgrade():
    op.execute(sa.text(
        "DELETE FROM products "
        "WHERE name IN ('iPhone 15', 'Gaming Laptop')"
    ))

    op.execute(sa.text(
        "DELETE FROM categories "
        "WHERE name = 'Laptops'"
    ))
