"""conversation enum type enabled

Revision ID: 2249a5159174
Revises: e6c0b05ccc22
Create Date: 2023-09-09 19:33:49.304062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2249a5159174'
down_revision = 'e6c0b05ccc22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('DIRECT', 'QA', 'GROUP', 'OPEN', name='conversationtype').create(op.get_bind())
    op.add_column('conversations', sa.Column('type', postgresql.ENUM('DIRECT', 'QA', 'GROUP', 'OPEN', name='conversationtype', create_type=False), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conversations', 'type')
    sa.Enum('DIRECT', 'QA', 'GROUP', 'OPEN', name='conversationtype').drop(op.get_bind())
    # ### end Alembic commands ###