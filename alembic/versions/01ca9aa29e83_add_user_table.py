"""Add user table

Revision ID: 01ca9aa29e83
Revises: 34e47e4f05c0
Create Date: 2022-08-28 21:47:28.544024

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01ca9aa29e83'
down_revision = '34e47e4f05c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                sa.Column("id", sa.Integer(), nullable=False),
                sa.Column("email", sa.String(), nullable=False),
                sa.Column("password", sa.String(), nullable=False),
                sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
