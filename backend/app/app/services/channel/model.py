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


class ChannelType(enum.Enum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class Channel(Base):
    __tablename__ = "channels"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    name = Column(String)
    type = Column(ENUM(ChannelType), default=ChannelType.TEXT.value)
    profileId = Column(UUID, ForeignKey('profiles.id'), nullable=False)
    serverId = Column(UUID, ForeignKey('servers.id'), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relations
    messages = relationship("Message", backref="channel")
    members = relationship("MemberOnChannel", backref="channel")

class MemberOnChannel(Base):
    __tablename__ = "members_on_channels"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    memberId = Column(UUID, ForeignKey('members.id'), nullable=False)
    channelId = Column(UUID, ForeignKey('channels.id'), nullable=False)
    assignedAt = Column(DateTime, default=datetime.utcnow)
    assignedBy = Column(String)

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID, primary_key=True, default=Text("gen_random_uuid()"))
    content = Column(TEXT)
    fileUrl = Column(TEXT)
    memberId = Column(UUID, ForeignKey('members.id'), nullable=False)
    channelId = Column(UUID, ForeignKey('channels.id'), nullable=False)
    deleted = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
