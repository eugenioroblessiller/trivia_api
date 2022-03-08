"""empty message

Revision ID: 012f8ef91292
Revises: 5b8ffa2c8106
Create Date: 2022-03-07 23:59:47.820455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012f8ef91292'
down_revision = '5b8ffa2c8106'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_genres')
    op.drop_table('venue_genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_genres',
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genere_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['genere_id'], ['genere.id'], name='venue_genres_genere_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='venue_genres_venue_id_fkey'),
    sa.PrimaryKeyConstraint('venue_id', 'genere_id', name='venue_genres_pkey')
    )
    op.create_table('artist_genres',
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genere_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='artist_genres_artist_id_fkey'),
    sa.ForeignKeyConstraint(['genere_id'], ['genere.id'], name='artist_genres_genere_id_fkey'),
    sa.PrimaryKeyConstraint('artist_id', 'genere_id', name='artist_genres_pkey')
    )
    # ### end Alembic commands ###
