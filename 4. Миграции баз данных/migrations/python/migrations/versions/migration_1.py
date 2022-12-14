"""empty message

Revision ID: c43b5e3e04d4
Revises: 
Create Date: 2022-08-07 12:58:12.526305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c43b5e3e04d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('login', sa.VARCHAR(length=50), nullable=False),
    sa.Column('city', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__driver')),
    sa.UniqueConstraint('id', name=op.f('uq__driver__id')),
    sa.UniqueConstraint('login', name=op.f('uq__driver__login'))
    )
    op.create_table('spaceship_manufacturer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('company_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('country', sa.VARCHAR(length=50), nullable=True),
    sa.Column('nasdaq_code', sa.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__spaceship_manufacturer')),
    sa.UniqueConstraint('id', name=op.f('uq__spaceship_manufacturer__id'))
    )
    op.create_table('spaceship_model',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('manufacturer_id', sa.INTEGER(), nullable=False),
    sa.Column('model_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('horsepower', postgresql.DOUBLE_PRECISION(), nullable=False),
    sa.CheckConstraint('horsepower BETWEEN 170000000 AND 240000000', name=op.f('ck__spaceship_model__valid_values')),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['spaceship_manufacturer.id'], name=op.f('fk__spaceship_model__manufacturer_id__spaceship_manufacturer')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__spaceship_model')),
    sa.UniqueConstraint('id', name=op.f('uq__spaceship_model__id'))
    )
    op.create_table('spaceship',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ship_number', sa.VARCHAR(length=50), nullable=False),
    sa.Column('model_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['spaceship_model.id'], name=op.f('fk__spaceship__model_id__spaceship_model')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__spaceship')),
    sa.UniqueConstraint('id', name=op.f('uq__spaceship__id'))
    )
    op.create_table('spaceship_rent',
    sa.Column('driver_id', sa.INTEGER(), nullable=False),
    sa.Column('spaceship_id', sa.INTEGER(), nullable=False),
    sa.Column('rent_start', postgresql.TIMESTAMP(), nullable=False),
    sa.Column('rent_end', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.id'], name=op.f('fk__spaceship_rent__driver_id__driver')),
    sa.ForeignKeyConstraint(['spaceship_id'], ['spaceship.id'], name=op.f('fk__spaceship_rent__spaceship_id__spaceship')),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spaceship_rent')
    op.drop_table('spaceship')
    op.drop_table('spaceship_model')
    op.drop_table('spaceship_manufacturer')
    op.drop_table('driver')
    # ### end Alembic commands ###
