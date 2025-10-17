from typing import Dict, Any, List
from schema.challenge import ChallengeStatus, DifficultyLevel
import json
import hashlib

def validate_challenge_submission(challenge_id: str, submission: Dict[str, Any]) -> bool:
    """Validate a challenge submission"""
    # This would contain challenge-specific validation logic
    # For now, returning True as placeholder
    return True

def calculate_score(challenge_id: str, submission: Dict[str, Any], max_score: int = 100) -> int:
    """Calculate score for a challenge submission"""
    # This would contain scoring logic based on challenge type
    # For now, returning max_score as placeholder
    return max_score

def get_challenge_feedback(challenge_id: str, submission: Dict[str, Any], is_correct: bool) -> str:
    """Generate feedback for a challenge submission"""
    if is_correct:
        return "Congratulations! You've successfully completed this challenge."
    else:
        return "Your submission needs improvement. Please review the challenge requirements and try again."

def hash_solution(solution: Dict[str, Any]) -> str:
    """Hash a challenge solution for secure storage"""
    solution_str = json.dumps(solution, sort_keys=True)
    return hashlib.sha256(solution_str.encode()).hexdigest()

def verify_solution(submission: Dict[str, Any], hashed_solution: str) -> bool:
    """Verify if submission matches the expected solution"""
    submission_hash = hash_solution(submission)
    return submission_hash == hashed_solution

def get_difficulty_points(difficulty: DifficultyLevel) -> int:
    """Get base points for difficulty level"""
    points_map = {
        DifficultyLevel.BEGINNER: 50,
        DifficultyLevel.INTERMEDIATE: 100,
        DifficultyLevel.ADVANCED: 200
    }
    return points_map.get(difficulty, 100)

def calculate_user_progress(completed_challenges: List[Dict], total_challenges: int) -> Dict[str, Any]:
    """Calculate user's overall progress"""
    if total_challenges == 0:
        return {
            "completion_percentage": 0,
            "total_points": 0,
            "challenges_by_difficulty": {}
        }
    
    completed_count = len(completed_challenges)
    completion_percentage = (completed_count / total_challenges) * 100
    total_points = sum(challenge.get("points", 0) for challenge in completed_challenges)
    
    # Group by difficulty
    difficulty_stats = {}
    for challenge in completed_challenges:
        difficulty = challenge.get("difficulty", "unknown")
        if difficulty not in difficulty_stats:
            difficulty_stats[difficulty] = 0
        difficulty_stats[difficulty] += 1
    
    return {
        "completion_percentage": round(completion_percentage, 2),
        "total_points": total_points,
        "completed_challenges": completed_count,
        "total_challenges": total_challenges,
        "challenges_by_difficulty": difficulty_stats
    }