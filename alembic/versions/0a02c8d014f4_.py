"""Add last few columns to posts table

Revision ID: 0a02c8d014f4
Revises: abfaad4f037a
Create Date: 2022-08-28 22:23:07.207140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a02c8d014f4'
down_revision = 'abfaad4f037a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
