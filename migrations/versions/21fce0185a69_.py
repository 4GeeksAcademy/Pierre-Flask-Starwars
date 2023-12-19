"""empty message

Revision ID: 21fce0185a69
Revises: a5cffa318ac2
Create Date: 2023-12-14 00:47:50.902849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21fce0185a69'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('about', sa.String(length=120), nullable=True),
    sa.Column('favorites_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorites_id'], ['favorites.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('about'),
    sa.UniqueConstraint('name')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('about', sa.String(length=120), nullable=True),
    sa.Column('favorites_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorites_id'], ['favorites.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets')
    op.drop_table('people')
    op.drop_table('favorites')
    # ### end Alembic commands ###
