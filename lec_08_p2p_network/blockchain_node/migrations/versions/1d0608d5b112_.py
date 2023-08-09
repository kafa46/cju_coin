"""empty message

Revision ID: 1d0608d5b112
Revises: 
Create Date: 2023-08-09 11:57:11.946699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d0608d5b112'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mining_node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=50), nullable=False),
    sa.Column('port', sa.String(length=50), nullable=False),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mining_node')
    # ### end Alembic commands ###