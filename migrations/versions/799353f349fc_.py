"""empty message

Revision ID: 799353f349fc
Revises: baf38df78d93
Create Date: 2019-03-13 09:22:29.602883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799353f349fc'
down_revision = 'baf38df78d93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('month_c',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month_name', sa.String(length=20), nullable=False),
    sa.Column('month_letter', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('month')
    op.add_column('options', sa.Column('contract', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'options', 'month_c', ['contract'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'options', type_='foreignkey')
    op.drop_column('options', 'contract')
    op.create_table('month',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('month_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('month_letter', sa.VARCHAR(length=8), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='month_pkey')
    )
    op.drop_table('month_c')
    # ### end Alembic commands ###