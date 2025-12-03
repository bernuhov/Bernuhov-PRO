"""
User progress tracking for the educational pipeline.
Stores user progress in a simple JSON file-based system.
"""

import json
import os
import logging
from datetime import datetime

PROGRESS_FILE = "user_progress.json"

# Set up logging
logger = logging.getLogger(__name__)

def load_progress():
    """Load user progress from file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_progress(progress_data):
    """Save user progress to file."""
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress_data, f, indent=2)
    except (IOError, OSError) as e:
        logger.error(f"Failed to save user progress: {e}")
        raise

def initialize_user(user_id):
    """Initialize a new user in the educational pipeline."""
    progress = load_progress()
    
    if str(user_id) not in progress:
        progress[str(user_id)] = {
            "current_lesson": 1,
            "completed_lessons": [],
            "quiz_scores": {},
            "started_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        save_progress(progress)
    
    return progress[str(user_id)]

def get_user_progress(user_id):
    """Get progress for a specific user."""
    progress = load_progress()
    return progress.get(str(user_id))

def update_user_lesson(user_id, lesson_id):
    """Update user's current lesson."""
    progress = load_progress()
    user_data = progress.get(str(user_id))
    
    if user_data:
        user_data["current_lesson"] = lesson_id
        user_data["last_activity"] = datetime.now().isoformat()
        save_progress(progress)

def complete_lesson(user_id, lesson_id, quiz_score=None):
    """Mark a lesson as completed for a user."""
    progress = load_progress()
    user_data = progress.get(str(user_id))
    
    if user_data:
        if lesson_id not in user_data["completed_lessons"]:
            user_data["completed_lessons"].append(lesson_id)
        
        if quiz_score is not None:
            user_data["quiz_scores"][str(lesson_id)] = quiz_score
        
        # Move to next lesson
        user_data["current_lesson"] = lesson_id + 1
        user_data["last_activity"] = datetime.now().isoformat()
        save_progress(progress)

def get_completed_lessons(user_id):
    """Get list of completed lessons for a user."""
    user_data = get_user_progress(user_id)
    if user_data:
        return user_data.get("completed_lessons", [])
    return []

def get_current_lesson(user_id):
    """Get the current lesson ID for a user."""
    user_data = get_user_progress(user_id)
    if user_data:
        return user_data.get("current_lesson", 1)
    return 1

def calculate_overall_progress(user_id, total_lessons):
    """Calculate overall progress percentage."""
    completed = get_completed_lessons(user_id)
    if total_lessons == 0:
        return 0
    return int((len(completed) / total_lessons) * 100)
