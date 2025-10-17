from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ChallengeStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ChallengeBase(BaseModel):
    title: str
    description: str
    difficulty: DifficultyLevel
    category: str
    points: int = 100
    is_active: bool = True

class ChallengeCreate(ChallengeBase):
    content: Dict[str, Any]  # Challenge-specific content
    solution: Optional[Dict[str, Any]] = None

class Challenge(ChallengeBase):
    id: str
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChallengeResponse(BaseModel):
    challenge_id: str
    user_id: int
    status: ChallengeStatus
    score: Optional[int] = None
    submission: Dict[str, Any]
    feedback: Optional[str] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserProgress(BaseModel):
    user_id: int
    total_challenges: int
    completed_challenges: int
    total_points: int
    earned_points: int
    progress_percentage: float
    challenges_by_difficulty: Dict[str, Dict[str, int]]