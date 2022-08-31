"""Add foriegn key to posts table

Revision ID: abfaad4f037a
Revises: 01ca9aa29e83
Create Date: 2022-08-28 22:12:25.124555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abfaad4f037a'
down_revision = '01ca9aa29e83'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', "posts", "users",  ['owner_id'], ['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
