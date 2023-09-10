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


class ConversationType(enum.Enum):
    DIRECT = "DIRECT"
    QA = "QA"
    GROUP = "GROUP"
    OPEN = "OPEN"

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

