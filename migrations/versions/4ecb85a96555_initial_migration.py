"""initial migration

Revision ID: 4ecb85a96555
Revises: 
Create Date: 2025-07-09 11:35:04.021138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ecb85a96555'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('heroes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('super_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('powers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hero_powers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strength', sa.String(length=20), nullable=False),
    sa.Column('hero_id', sa.Integer(), nullable=False),
    sa.Column('power_id', sa.Integer(), nullable=False),
    sa.CheckConstraint("strength IN ('Strong', 'Weak', 'Average')", name='check_strength'),
    sa.ForeignKeyConstraint(['hero_id'], ['heroes.id'], ),
    sa.ForeignKeyConstraint(['power_id'], ['powers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hero_powers')
    op.drop_table('powers')
    op.drop_table('heroes')
    # ### end Alembic commands ###
