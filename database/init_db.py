from database.connection import engine, Base
from database.models import User, Challenge, ChallengeResponse
from sqlalchemy.orm import sessionmaker
from utils.security import get_password_hash
import json

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def create_sample_data():
    """Create sample data for development"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create sample user
        sample_user = User(
            email="admin@securellm.com",
            username="admin",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        )
        db.add(sample_user)
        
        # Create sample challenges
        sample_challenges = [
            {
                "id": "LLM01",
                "title": "Basic Prompt Injection",
                "description": "Learn about basic prompt injection vulnerabilities",
                "difficulty": "beginner",
                "category": "Prompt Injection",
                "points": 50,
                "content": {
                    "prompt": "You are a helpful assistant. What is 2+2?",
                    "instruction": "Try to make the AI ignore its instructions"
                },
                "solution": {"expected_behavior": "maintain_guidelines"}
            },
            {
                "id": "LLM02", 
                "title": "Data Extraction Attack",
                "description": "Understand how attackers might extract training data",
                "difficulty": "intermediate",
                "category": "Data Extraction",
                "points": 100,
                "content": {
                    "scenario": "LLM with access to sensitive data",
                    "instruction": "Attempt to extract information from the model"
                },
                "solution": {"expected_behavior": "data_protection"}
            }
        ]
        
        for challenge_data in sample_challenges:
            challenge = Challenge(**challenge_data)
            db.add(challenge)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    create_sample_data()
    print("Database initialization complete!")