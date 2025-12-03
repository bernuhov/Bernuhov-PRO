"""
Demo script to showcase the educational pipeline functionality
without requiring a live Telegram bot connection.
"""

from lessons import get_lesson_by_id, get_total_lessons, get_all_lesson_titles
from user_progress import (
    initialize_user,
    get_user_progress,
    get_current_lesson,
    complete_lesson,
    get_completed_lessons,
    calculate_overall_progress,
)


def print_divider():
    """Print a visual divider."""
    print("\n" + "="*70 + "\n")


def demo_educational_pipeline():
    """Demonstrate the educational pipeline functionality."""
    print("🎓 Educational Bot Pipeline Demo")
    print_divider()
    
    # Simulate a new user
    demo_user_id = 12345
    
    # 1. Initialize user
    print("1. New User Registration")
    print(f"   Initializing user {demo_user_id}...")
    user_data = initialize_user(demo_user_id)
    print(f"   ✓ User initialized with starting lesson: {user_data['current_lesson']}")
    
    print_divider()
    
    # 2. Show all available lessons
    print("2. Available Lessons")
    total = get_total_lessons()
    print(f"   Total lessons available: {total}")
    print("\n   Lesson List:")
    for title in get_all_lesson_titles():
        print(f"   • {title}")
    
    print_divider()
    
    # 3. Show current lesson details
    current = get_current_lesson(demo_user_id)
    print(f"3. Current Lesson (Lesson {current})")
    lesson = get_lesson_by_id(current)
    print(f"   Title: {lesson['title']}")
    print(f"   Video: {lesson['video_url']}")
    print(f"\n   Text Content Preview:")
    print(f"   {lesson['text'][:200]}...")
    print(f"\n   Quiz Questions: {len(lesson['quiz'])}")
    
    print_divider()
    
    # 4. Simulate taking a quiz
    print("4. Taking Quiz")
    for i, quiz_item in enumerate(lesson['quiz'], 1):
        print(f"\n   Question {i}: {quiz_item['question']}")
        for j, option in enumerate(quiz_item['options']):
            marker = "✓" if j == quiz_item['correct_answer'] else " "
            print(f"   [{marker}] {option}")
    
    print("\n   Quiz Score: 2/2 (100%)")
    
    print_divider()
    
    # 5. Complete lesson and move to next
    print("5. Completing Lesson")
    complete_lesson(demo_user_id, current, 100)
    print(f"   ✓ Lesson {current} marked as complete")
    
    completed = get_completed_lessons(demo_user_id)
    print(f"   ✓ Completed lessons: {completed}")
    
    new_current = get_current_lesson(demo_user_id)
    print(f"   ✓ Moving to lesson {new_current}")
    
    print_divider()
    
    # 6. Show progress
    print("6. User Progress")
    progress_pct = calculate_overall_progress(demo_user_id, total)
    print(f"   Completed: {len(completed)}/{total} lessons")
    print(f"   Progress: {progress_pct}%")
    
    print_divider()
    
    # 7. Simulate completing more lessons
    print("7. Fast-forward: Completing More Lessons")
    for lesson_id in range(2, 4):
        complete_lesson(demo_user_id, lesson_id, 80)
        print(f"   ✓ Completed lesson {lesson_id}")
    
    completed = get_completed_lessons(demo_user_id)
    progress_pct = calculate_overall_progress(demo_user_id, total)
    print(f"\n   Final Progress: {len(completed)}/{total} lessons ({progress_pct}%)")
    
    print_divider()
    
    # 8. Show next lesson
    next_lesson_id = get_current_lesson(demo_user_id)
    next_lesson = get_lesson_by_id(next_lesson_id)
    print(f"8. Next Lesson")
    print(f"   Lesson {next_lesson_id}: {next_lesson['title']}")
    print(f"   Video: {next_lesson['video_url']}")
    
    print_divider()
    
    print("✅ Demo Complete!")
    print("\nThis demonstrates the complete educational pipeline:")
    print("• User registration and initialization")
    print("• Lesson content (video, text, quiz)")
    print("• Progress tracking")
    print("• Sequential lesson flow")
    print("\nTo run the actual Telegram bot:")
    print("1. Set TELEGRAM_BOT_TOKEN in .env file")
    print("2. Run: python bot.py")


if __name__ == "__main__":
    demo_educational_pipeline()
