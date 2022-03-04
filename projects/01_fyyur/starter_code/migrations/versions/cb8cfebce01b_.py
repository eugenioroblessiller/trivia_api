"""empty message

Revision ID: cb8cfebce01b
Revises: 9e6df0fba44f
Create Date: 2022-03-03 23:08:07.318786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8cfebce01b'
down_revision = '9e6df0fba44f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artist_genres_genere_id_fkey', 'artist_genres', type_='foreignkey')
    op.drop_constraint('artist_genres_artist_id_fkey', 'artist_genres', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('artist_genres_artist_id_fkey', 'artist_genres', 'Artist', ['artist_id'], ['id'])
    op.create_foreign_key('artist_genres_genere_id_fkey', 'artist_genres', 'Genre', ['genere_id'], ['id'])
    # ### end Alembic commands ###