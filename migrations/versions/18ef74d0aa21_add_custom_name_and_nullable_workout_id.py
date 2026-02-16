"""add custom_name and nullable workout_id

Revision ID: 18ef74d0aa21
Revises: 5213fc373b69
Create Date: 2026-02-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18ef74d0aa21'
down_revision = '5213fc373b69'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('workout_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('custom_name', sa.String(length=200), nullable=True))
        batch_op.alter_column('workout_id', existing_type=sa.Integer(), nullable=True)


def downgrade():
    with op.batch_alter_table('workout_logs', schema=None) as batch_op:
        batch_op.alter_column('workout_id', existing_type=sa.Integer(), nullable=False)
        batch_op.drop_column('custom_name')
