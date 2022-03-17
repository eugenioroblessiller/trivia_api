"""empty message

Revision ID: 5b8ffa2c8106
Revises: 462da8d726a4
Create Date: 2022-03-07 23:59:07.814968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b8ffa2c8106'
down_revision = '462da8d726a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    op.add_column('venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###