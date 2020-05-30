"""empty message

Revision ID: b142478e4777
Revises: 
Create Date: 2020-05-27 18:34:45.485423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b142478e4777'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('info', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('nickname', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('sex', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'sex')
    op.drop_column('users', 'nickname')
    op.drop_column('users', 'info')
    # ### end Alembic commands ###