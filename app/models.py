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


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
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


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # User -> Chat History

    chats = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete"
    )



# ===========================
# CHAT MESSAGE TABLE
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


    # Chat -> User

    user = relationship(
        "User",
        back_populates="chats"
    )