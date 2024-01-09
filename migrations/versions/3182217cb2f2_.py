"""empty message

Revision ID: 3182217cb2f2
Revises: ccc1a96bd129
Create Date: 2024-01-09 13:19:01.823801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3182217cb2f2'
down_revision = 'ccc1a96bd129'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=240), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
