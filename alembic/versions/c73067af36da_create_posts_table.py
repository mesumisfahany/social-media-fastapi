"""Create Posts Table

Revision ID: c73067af36da
Revises: 
Create Date: 2022-08-28 21:15:55.228639

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'c73067af36da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
     sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
     sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
