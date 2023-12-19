"""empty message

Revision ID: fb498ab2862b
Revises: 1f13984c3ed8
Create Date: 2023-12-19 00:06:35.697036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb498ab2862b'
down_revision = '1f13984c3ed8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorites_favorite_people_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_favorite_planet_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])
        batch_op.drop_column('favorite_people_id')
        batch_op.drop_column('favorite_planet_id')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint('people_favorites_id_fkey', type_='foreignkey')
        batch_op.drop_column('favorites_id')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint('planets_favorites_id_fkey', type_='foreignkey')
        batch_op.drop_column('favorites_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('planets_favorites_id_fkey', 'favorites', ['favorites_id'], ['id'])

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorites_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('people_favorites_id_fkey', 'favorites', ['favorites_id'], ['id'])

    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('favorite_people_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorites_favorite_planet_id_fkey', 'planets', ['favorite_planet_id'], ['id'])
        batch_op.create_foreign_key('favorites_favorite_people_id_fkey', 'people', ['favorite_people_id'], ['id'])
        batch_op.drop_column('people_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
