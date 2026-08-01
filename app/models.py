from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


# ===========================
# USER TABLE
# ===========================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    chats = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete"
    )


# ===========================
# CHAT TABLE
# ===========================

class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user_message = Column(
        String,
        nullable=False
    )

    ai_response = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="chats"
    )


# ===========================
# DOCTOR TABLE
# ===========================

class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    specialization = Column(
        String,
        nullable=False
    )

    experience = Column(
        Integer,
        nullable=False
    )

    qualification = Column(
        String,
        nullable=False
    )

    hospital = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    available_days = Column(
        String,
        nullable=True
    )

    available_time = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )