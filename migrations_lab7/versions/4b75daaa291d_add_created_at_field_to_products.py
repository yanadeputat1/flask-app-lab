"""Add created_at field to products

Revision ID: 4b75daaa291d
Revises: 752f4e27781f
Create Date: 2026-11-13 14:32:16.801167
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b75daaa291d'
down_revision = '752f4e27781f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("'2026-11-13 14:32:16'")
            )
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('created_at')
