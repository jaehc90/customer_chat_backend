"""chat model added

Revision ID: 81f83781fe93
Revises: ac495d2029da
Create Date: 2023-09-09 15:23:38.955112

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '81f83781fe93'
down_revision = 'ac495d2029da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_messages',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('conversations',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('memberIds', postgresql.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('userId', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('imageUrl', sa.TEXT(), nullable=True),
    sa.Column('email', sa.TEXT(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('userId')
    )
    op.create_table('servers',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('imageUrl', sa.Text(), nullable=True),
    sa.Column('inviteCode', sa.String(), nullable=False),
    sa.Column('profileId', postgresql.UUID(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profileId'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('inviteCode')
    )
    op.create_table('channels',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('profileId', postgresql.UUID(), nullable=False),
    sa.Column('serverId', postgresql.UUID(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profileId'], ['profiles.id'], ),
    sa.ForeignKeyConstraint(['serverId'], ['servers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('members',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('profileId', postgresql.UUID(), nullable=False),
    sa.Column('serverId', postgresql.UUID(), nullable=False),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profileId'], ['profiles.id'], ),
    sa.ForeignKeyConstraint(['serverId'], ['servers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('direct_messages',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('fileUrl', sa.Text(), nullable=True),
    sa.Column('memberId', postgresql.UUID(), nullable=False),
    sa.Column('conversationId', postgresql.UUID(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['conversationId'], ['conversations.id'], ),
    sa.ForeignKeyConstraint(['memberId'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('members_on_channels',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('memberId', postgresql.UUID(), nullable=False),
    sa.Column('channelId', postgresql.UUID(), nullable=False),
    sa.Column('assignedAt', sa.DateTime(), nullable=True),
    sa.Column('assignedBy', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['channelId'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['memberId'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('members_on_conversations',
    sa.Column('conversationId', postgresql.UUID(), nullable=False),
    sa.Column('memberId', postgresql.UUID(), nullable=False),
    sa.Column('assignedAt', sa.DateTime(), nullable=True),
    sa.Column('assignedBy', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['conversationId'], ['conversations.id'], ),
    sa.ForeignKeyConstraint(['memberId'], ['members.id'], ),
    sa.PrimaryKeyConstraint('conversationId', 'memberId')
    )
    op.create_table('messages',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.Column('fileUrl', sa.TEXT(), nullable=True),
    sa.Column('memberId', postgresql.UUID(), nullable=False),
    sa.Column('channelId', postgresql.UUID(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channelId'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['memberId'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('seen_members_on_chat_messages',
    sa.Column('chatMessageId', postgresql.UUID(), nullable=False),
    sa.Column('memberId', postgresql.UUID(), nullable=False),
    sa.Column('assignedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chatMessageId'], ['chat_messages.id'], ),
    sa.ForeignKeyConstraint(['memberId'], ['members.id'], ),
    sa.PrimaryKeyConstraint('chatMessageId', 'memberId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seen_members_on_chat_messages')
    op.drop_table('messages')
    op.drop_table('members_on_conversations')
    op.drop_table('members_on_channels')
    op.drop_table('direct_messages')
    op.drop_table('members')
    op.drop_table('channels')
    op.drop_table('servers')
    op.drop_table('profiles')
    op.drop_table('conversations')
    op.drop_table('chat_messages')
    # ### end Alembic commands ###