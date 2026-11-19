"""Add active field to products

Revision ID: 752f4e27781f
Revises: 16302ddbe57e
Create Date: 2026-11-13 14:24:58.346717
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '752f4e27781f'
down_revision = '16302ddbe57e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'active',
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('active')
