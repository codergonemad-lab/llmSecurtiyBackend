from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    challenge_responses = relationship("ChallengeResponse", back_populates="user")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    difficulty = Column(String, nullable=False)  # beginner, intermediate, advanced
    category = Column(String, nullable=False)
    points = Column(Integer, default=100)
    content = Column(JSON)  # Challenge-specific content
    solution = Column(JSON)  # Challenge solution (encrypted/hashed)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    responses = relationship("ChallengeResponse", back_populates="challenge")

class ChallengeResponse(Base):
    __tablename__ = "challenge_responses"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(String, ForeignKey("challenges.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)  # not_started, in_progress, completed, failed
    score = Column(Integer)
    submission = Column(JSON)
    feedback = Column(Text)
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="challenge_responses")
    challenge = relationship("Challenge", back_populates="responses")