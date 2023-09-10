from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Boolean, Text, Table
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy.dialects.postgresql import UUID, TEXT, ARRAY
from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import ENUM

from typing import TYPE_CHECKING, Any

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from app.db.base_class import Base


# # Setup and finalize
# DATABASE_URL = "your_database_url_here"
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)



# Base = declarative_base()

# Enums
# class MemberRole(ENUM):
#     ADMIN = "ADMIN"
#     MODERATOR = "MODERATOR"
#     GUEST = "GUEST"
    
# MemberRoleEnum = ENUM('ADMIN', 'MODERATOR', 'GUEST', name='memberrole', create_type=False)


# class ChannelType(enum.Enum):
#     TEXT = "TEXT"
#     AUDIO = "AUDIO"
#     VIDEO = "VIDEO"

class ConversationType(enum.Enum):
    DIRECT = "DIRECT"
    QA = "QA"
    GROUP = "GROUP"
    OPEN = "OPEN"

# Models
# class Profile(Base):
#     __tablename__ = "profiles"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     userId = Column(String, unique=True)
#     name = Column(String)
#     imageUrl = Column(TEXT)
#     email = Column(TEXT)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     # Relations
#     servers = relationship("Server", backref="profile")
#     members = relationship("Member", backref="profile")
#     channels = relationship("Channel", backref="profile")

# class Server(Base):
#     __tablename__ = "servers"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     name = Column(String, nullable=False)
#     imageUrl = Column(Text)
#     inviteCode = Column(String, unique=True, nullable=False)
#     profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     profile = relationship("Profile", back_populates="servers")
#     members = relationship("Member", back_populates="server")
#     channels = relationship("Channel", back_populates="server")
#     conversations = relationship("Conversation", back_populates="server")

# class Member(Base):
#     __tablename__ = "members"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     role = Column(MemberRoleEnum, default=MemberRole.GUEST, nullable=True)
#     profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
#     serverId = Column(UUID, ForeignKey('servers.id'), nullable=False)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     profile = relationship("Profile", back_populates="members")
#     server = relationship("Server", back_populates="members")
#     messages = relationship("Message", back_populates="member")
#     directMessages = relationship("DirectMessage", back_populates="member")
#     initiatedConversations = relationship("Conversation", foreign_keys="Conversation.memberOneId", back_populates="memberOne")
#     receivedConversations = relationship("Conversation", foreign_keys="Conversation.memberTwoId", back_populates="memberTwo")
#     chatMessages = relationship("ChatMessage", back_populates="sender")
#     seenChatMessages = relationship("SeenMemberOnChatMessage", back_populates="member")
#     memberOnChannels = relationship("MemberOnChannel", back_populates="member")
#     memberOnConversations = relationship("MemberOnConversation", back_populates="member")


# class Channel(Base):
#     __tablename__ = "channels"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     name = Column(String)
#     type = Column(ENUM(ChannelType), default=ChannelType.TEXT.value)
#     profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
#     serverId = Column(UUID, ForeignKey('servers.id'), nullable=False)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     # Relations
#     messages = relationship("Message", backref="channel")
#     members = relationship("MemberOnChannel", backref="channel")

# class MemberOnChannel(Base):
#     __tablename__ = "members_on_channels"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     memberId = Column(UUID, ForeignKey('members.id'), nullable=False)
#     channelId = Column(UUID, ForeignKey('channels.id'), nullable=False)
#     assignedAt = Column(DateTime, default=datetime.utcnow)
#     assignedBy = Column(String)

# class Message(Base):
#     __tablename__ = "messages"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     content = Column(TEXT)
#     fileUrl = Column(TEXT)
#     memberId = Column(UUID, ForeignKey('members.id'), nullable=False)
#     channelId = Column(UUID, ForeignKey('channels.id'), nullable=False)
#     deleted = Column(Boolean, default=False)
#     createdAt = Column(DateTime, default=datetime.utcnow)
#     updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# class Conversation(Base):
#     __tablename__ = "conversations"

#     id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
#     # ... other fields
#     type = Column(ENUM(ConversationType), default=ConversationType.GROUP)
#     memberIds = Column(ARRAY(String))
#     # ... remaining fields and relationships

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    createdAt = Column(DateTime, default=datetime.utcnow)
    lastMessageAt = Column(DateTime, default=datetime.utcnow)
    serverId = Column(UUID, ForeignKey('servers.id'), nullable=False)
    creatorId = Column(UUID, ForeignKey('members.id'))
    type = Column(ENUM(ConversationType), default=ConversationType.GROUP)
    name = Column(String)
    isGroup = Column(Boolean)
    # memberIds = Column(ARRAY(UUID))
    memberOneId = Column(UUID, ForeignKey('members.id'))
    memberTwoId = Column(UUID, ForeignKey('members.id'))
    messageIds = Column(ARRAY(UUID))
    directMessageIds = Column(ARRAY(UUID))

    # Relationships
    server = relationship("Server", back_populates="conversations")
    creator = relationship("Member", backref=backref("created_conversations", uselist=True), foreign_keys=[creatorId])
    memberOne = relationship("Member", backref=backref("initiated_conversations", uselist=True), foreign_keys=[memberOneId])
    memberTwo = relationship("Member", backref=backref("received_conversations", uselist=True), foreign_keys=[memberTwoId])
    # members = relationship("MemberOnConversation", back_populates="conversation")
    members = relationship("Member", secondary="members_on_conversations", back_populates="conversations")

    # messages = relationship("ChatMessage", back_populates="conversation")
    # directMessages = relationship("DirectMessage", back_populates="conversation")


class MemberOnConversation(Base):
    __tablename__ = "members_on_conversations"

    # This represents a composite primary key in SQLAlchemy
    conversationId = Column(UUID, ForeignKey('conversations.id'), primary_key=True)
    memberId = Column(UUID, ForeignKey('members.id'), primary_key=True)
    assignedAt = Column(DateTime, default=datetime.utcnow)
    assignedBy = Column(String)

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    # ... other fields and relationships

class SeenMemberOnChatMessage(Base):
    __tablename__ = "seen_members_on_chat_messages"

    chatMessageId = Column(UUID, ForeignKey('chat_messages.id'), primary_key=True)
    memberId = Column(UUID, ForeignKey('members.id'), primary_key=True)
    assignedAt = Column(DateTime, default=datetime.utcnow)

class DirectMessage(Base):
    __tablename__ = "direct_messages"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    content = Column(Text, nullable=False)
    fileUrl = Column(Text)
    memberId = Column(UUID, ForeignKey('members.id'), nullable=False)
    conversationId = Column(UUID, ForeignKey('conversations.id'), nullable=False)
    deleted = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    member = relationship("Member", back_populates="directMessages")
    conversation = relationship("Conversation", back_populates="directMessages")


# ... [Setup and finalize code]

