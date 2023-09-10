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


# Base = declarative_base()

# Enums
class MemberRole(ENUM):
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    GUEST = "GUEST"

MemberRoleEnum = ENUM('ADMIN', 'MODERATOR', 'GUEST', name='memberrole', create_type=False)


# Models
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    userId = Column(String, unique=True)
    name = Column(String)
    imageUrl = Column(TEXT)
    email = Column(TEXT)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relations
    servers = relationship("Server", backref="profile")
    members = relationship("Member", backref="profile")
    channels = relationship("Channel", backref="profile")

class Server(Base):
    __tablename__ = "servers"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    imageUrl = Column(Text)
    inviteCode = Column(String, unique=True, nullable=False)
    profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("Profile", back_populates="servers")
    members = relationship("Member", back_populates="server")
    channels = relationship("Channel", back_populates="server")
    conversations = relationship("Conversation", back_populates="server")

class Member(Base):
    __tablename__ = "members"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    role = Column(MemberRoleEnum, default=MemberRole.GUEST, nullable=True)
    profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
    serverId = Column(UUID, ForeignKey('servers.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("Profile", back_populates="members")
    server = relationship("Server", back_populates="members")
    messages = relationship("Message", back_populates="member")
    directMessages = relationship("DirectMessage", back_populates="member")
    initiatedConversations = relationship("Conversation", foreign_keys="Conversation.memberOneId", back_populates="memberOne")
    receivedConversations = relationship("Conversation", foreign_keys="Conversation.memberTwoId", back_populates="memberTwo")
    chatMessages = relationship("ChatMessage", back_populates="sender")
    seenChatMessages = relationship("SeenMemberOnChatMessage", back_populates="member")
    memberOnChannels = relationship("MemberOnChannel", back_populates="member")
    # memberOnConversations = relationship("MemberOnConversation", back_populates="member")
    conversations = relationship("Conversation", secondary="members_on_conversations", back_populates="members")


