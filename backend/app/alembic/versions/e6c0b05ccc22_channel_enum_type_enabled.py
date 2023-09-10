"""channel enum type enabled

Revision ID: e6c0b05ccc22
Revises: 72396746d801
Create Date: 2023-09-09 19:30:19.007840

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e6c0b05ccc22'
down_revision = '72396746d801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('TEXT', 'AUDIO', 'VIDEO', name='channeltype').create(op.get_bind())
    op.add_column('channels', sa.Column('type', postgresql.ENUM('TEXT', 'AUDIO', 'VIDEO', name='channeltype', create_type=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('channels', 'type')
    sa.Enum('TEXT', 'AUDIO', 'VIDEO', name='channeltype').drop(op.get_bind())
    # ### end Alembic commands ###
