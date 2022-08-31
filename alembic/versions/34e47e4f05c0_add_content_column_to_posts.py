"""Add content column to posts

Revision ID: 34e47e4f05c0
Revises: c73067af36da
Create Date: 2022-08-28 21:42:15.915351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34e47e4f05c0'
down_revision = 'c73067af36da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
