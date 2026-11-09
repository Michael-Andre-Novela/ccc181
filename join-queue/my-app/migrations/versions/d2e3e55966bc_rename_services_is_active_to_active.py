"""rename services is_active to active

Revision ID: d2e3e55966bc
Revises: cd506a18ff29
Create Date: 2026-11-09 05:28:53.140495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2e3e55966bc'
down_revision = 'cd506a18ff29'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.alter_column(
            'is_active',
            new_column_name='active'
        )


def downgrade():
    with op.batch_alter_table('services', schema=None) as batch_op:
        batch_op.alter_column(
            'active',
            new_column_name='is_active'
        )