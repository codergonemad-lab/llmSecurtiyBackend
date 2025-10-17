from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import os

from database.connection import get_db
from schema.challenge import Challenge, ChallengeCreate, ChallengeResponse
from schema.user import User
from utils.auth import get_current_user

router = APIRouter()

# In-memory storage for user progress (replace with database in production)
user_progress = {}

def load_challenge_from_json(challenge_id: str) -> Dict[Any, Any]:
    """Load challenge data from JSON file"""
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "json", f"{challenge_id}.json")
    
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail=f"Challenge {challenge_id} not found")
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_available_challenges() -> List[str]:
    """Get list of available challenge IDs"""
    json_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "json")
    challenge_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    return [f.replace('.json', '') for f in challenge_files]

def get_next_question_for_user(challenge_id: str, user_id: str = "default") -> Dict[Any, Any]:
    """Get the next question for a user in a specific challenge"""
    challenge_data = load_challenge_from_json(challenge_id)
    questions = challenge_data.get("questions", [])
    
    # Get user's progress for this challenge
    user_key = f"{user_id}_{challenge_id}"
    completed_questions = user_progress.get(user_key, [])
    
    # Find next unanswered question
    for question in questions:
        if question["questionNumber"] not in completed_questions:
            return question
    
    # If all questions completed
    return None

@router.get("/", response_model=List[Dict])
async def get_challenges():
    """Get list of all available challenges"""
    try:
        available_challenges = get_available_challenges()
        challenges = []
        
        for challenge_id in available_challenges:
            challenge_data = load_challenge_from_json(challenge_id)
            challenge_info = {
                "id": challenge_id,
                "title": f"LLM Security Challenge {challenge_id.upper()}",
                "description": f"Learn about LLM security vulnerabilities through {challenge_id.upper()}",
                "total_questions": len(challenge_data.get("questions", [])),
                "difficulty": "Intermediate"
            }
            challenges.append(challenge_info)
        
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{challenge_id}/current-question")
async def get_current_question(
    challenge_id: str,
    user_id: str = "default"
):
    """Get the current question for a user in a specific challenge"""
    try:
        next_question = get_next_question_for_user(challenge_id, user_id)
        
        if next_question is None:
            return {
                "message": "Challenge completed!",
                "completed": True,
                "progress": get_user_challenge_progress(challenge_id, user_id)
            }
        
        # Return question without correct answers
        return {
            "questionNumber": next_question["questionNumber"],
            "question": next_question["question"],
            "answerOptions": [
                {
                    "text": option["text"],
                    "index": idx
                } for idx, option in enumerate(next_question["answerOptions"])
            ],
            "hint": next_question.get("hint"),
            "completed": False,
            "progress": get_user_challenge_progress(challenge_id, user_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{challenge_id}/submit")
async def submit_answer(
    challenge_id: str,
    submission: Dict[str, Any],
    user_id: str = "default"
):
    """Submit answer for current question"""
    try:
        question_number = submission.get("questionNumber")
        selected_answer_index = submission.get("selectedAnswer")
        
        if question_number is None or selected_answer_index is None:
            raise HTTPException(status_code=400, detail="Missing questionNumber or selectedAnswer")
        
        # Load challenge data
        challenge_data = load_challenge_from_json(challenge_id)
        questions = challenge_data.get("questions", [])
        
        # Find the question
        current_question = None
        for q in questions:
            if q["questionNumber"] == question_number:
                current_question = q
                break
        
        if not current_question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Check if answer is correct
        answer_options = current_question["answerOptions"]
        if selected_answer_index >= len(answer_options):
            raise HTTPException(status_code=400, detail="Invalid answer index")
        
        selected_option = answer_options[selected_answer_index]
        is_correct = selected_option["isCorrect"]
        
        # Update user progress
        user_key = f"{user_id}_{challenge_id}"
        if user_key not in user_progress:
            user_progress[user_key] = []
        
        if question_number not in user_progress[user_key]:
            user_progress[user_key].append(question_number)
        
        # Prepare response
        response = {
            "correct": is_correct,
            "explanation": selected_option["rationale"],
            "correctAnswer": None,
            "progress": get_user_challenge_progress(challenge_id, user_id)
        }
        
        # If incorrect, show the correct answer
        if not is_correct:
            for idx, option in enumerate(answer_options):
                if option["isCorrect"]:
                    response["correctAnswer"] = {
                        "index": idx,
                        "text": option["text"],
                        "rationale": option["rationale"]
                    }
                    break
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/progress")
async def get_user_progress_all(user_id: str = "default"):
    """Get user's progress across all challenges"""
    try:
        available_challenges = get_available_challenges()
        progress_data = {}
        
        for challenge_id in available_challenges:
            progress_data[challenge_id] = get_user_challenge_progress(challenge_id, user_id)
        
        return progress_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user_challenge_progress(challenge_id: str, user_id: str = "default") -> Dict[str, Any]:
    """Get user's progress for a specific challenge"""
    try:
        challenge_data = load_challenge_from_json(challenge_id)
        total_questions = len(challenge_data.get("questions", []))
        
        user_key = f"{user_id}_{challenge_id}"
        completed_questions = len(user_progress.get(user_key, []))
        
        return {
            "completed": completed_questions,
            "total": total_questions,
            "percentage": round((completed_questions / total_questions) * 100, 2) if total_questions > 0 else 0,
            "is_completed": completed_questions >= total_questions
        }
    except Exception:
        return {
            "completed": 0,
            "total": 0,
            "percentage": 0,
            "is_completed": False
        }