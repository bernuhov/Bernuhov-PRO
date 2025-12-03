"""
Educational Telegram Bot - Main Entry Point
Implements an educational pipeline with video lessons, texts, and quizzes.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from lessons import get_lesson_by_id, get_total_lessons, get_all_lesson_titles
from user_progress import (
    initialize_user,
    get_user_progress,
    get_current_lesson,
    complete_lesson,
    get_completed_lessons,
    calculate_overall_progress,
)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Quiz state storage
user_quiz_state = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command - Put new users into educational pipeline."""
    user = update.effective_user
    user_id = user.id
    
    # Initialize user in the educational pipeline
    user_data = initialize_user(user_id)
    
    welcome_message = f"""
👋 Welcome to the Educational Bot, {user.first_name}!

🎓 You're now in our educational pipeline!

This bot will guide you through a series of programming lessons. Each lesson includes:
📹 Video content
📝 Text explanations
❓ Short quizzes to test your knowledge

Your progress will be saved, so you can learn at your own pace!

Use /menu to see available commands.
Use /lesson to start your first lesson!
    """
    
    await update.message.reply_text(welcome_message)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the main menu."""
    keyboard = [
        [InlineKeyboardButton("📚 Start/Continue Lesson", callback_data="continue_lesson")],
        [InlineKeyboardButton("📊 My Progress", callback_data="show_progress")],
        [InlineKeyboardButton("📋 All Lessons", callback_data="all_lessons")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    menu_text = """
🎓 Educational Bot Menu

Choose an option:
    """
    
    if update.callback_query:
        await update.callback_query.message.edit_text(menu_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(menu_text, reply_markup=reply_markup)


async def show_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: int) -> None:
    """Display a specific lesson."""
    lesson = get_lesson_by_id(lesson_id)
    query = update.callback_query
    
    if not lesson:
        await query.message.edit_text("❌ Lesson not found.")
        return
    
    lesson_text = f"""
📚 **Lesson {lesson['id']}: {lesson['title']}**

📹 **Video:** {lesson['video_url']}

📝 **Content:**
{lesson['text']}

Ready to test your knowledge?
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Take Quiz", callback_data=f"quiz_{lesson_id}")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(lesson_text, reply_markup=reply_markup, parse_mode="Markdown")


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: int) -> None:
    """Start a quiz for a specific lesson."""
    lesson = get_lesson_by_id(lesson_id)
    query = update.callback_query
    user_id = update.effective_user.id
    
    if not lesson:
        await query.message.edit_text("❌ Lesson not found.")
        return
    
    # Initialize quiz state
    user_quiz_state[user_id] = {
        "lesson_id": lesson_id,
        "current_question": 0,
        "correct_answers": 0,
        "total_questions": len(lesson["quiz"])
    }
    
    await show_quiz_question(update, context)


async def show_quiz_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the current quiz question."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    quiz_state = user_quiz_state.get(user_id)
    if not quiz_state:
        await query.message.edit_text("❌ Quiz state not found. Please start over.")
        return
    
    lesson = get_lesson_by_id(quiz_state["lesson_id"])
    question_idx = quiz_state["current_question"]
    
    if question_idx >= len(lesson["quiz"]):
        # Quiz completed
        await finish_quiz(update, context)
        return
    
    question_data = lesson["quiz"][question_idx]
    
    question_text = f"""
❓ **Question {question_idx + 1} of {quiz_state['total_questions']}**

{question_data['question']}
    """
    
    keyboard = []
    for i, option in enumerate(question_data["options"]):
        keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{i}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(question_text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer_idx: int) -> None:
    """Handle a quiz answer."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    quiz_state = user_quiz_state.get(user_id)
    if not quiz_state:
        await query.answer("❌ Quiz state not found. Please start over.")
        return
    
    lesson = get_lesson_by_id(quiz_state["lesson_id"])
    question_data = lesson["quiz"][quiz_state["current_question"]]
    
    is_correct = answer_idx == question_data["correct_answer"]
    
    if is_correct:
        quiz_state["correct_answers"] += 1
        await query.answer("✅ Correct!", show_alert=True)
    else:
        correct_option = question_data["options"][question_data["correct_answer"]]
        await query.answer(f"❌ Wrong! Correct answer: {correct_option}", show_alert=True)
    
    # Move to next question
    quiz_state["current_question"] += 1
    await show_quiz_question(update, context)


async def finish_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Finish the quiz and show results."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    quiz_state = user_quiz_state.get(user_id)
    if not quiz_state:
        return
    
    lesson_id = quiz_state["lesson_id"]
    correct = quiz_state["correct_answers"]
    total = quiz_state["total_questions"]
    percentage = int((correct / total) * 100)
    
    # Save progress
    complete_lesson(user_id, lesson_id, percentage)
    
    # Clear quiz state
    if user_id in user_quiz_state:
        del user_quiz_state[user_id]
    
    result_text = f"""
🎉 **Quiz Complete!**

Score: {correct}/{total} ({percentage}%)

{"🌟 Excellent work!" if percentage >= 80 else "💪 Good effort! Review the material and try again if needed."}

Lesson {lesson_id} completed!
    """
    
    total_lessons = get_total_lessons()
    current = get_current_lesson(user_id)
    
    keyboard = []
    if current <= total_lessons:
        keyboard.append([InlineKeyboardButton("➡️ Next Lesson", callback_data=f"lesson_{current}")])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")


async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user's progress."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    user_data = get_user_progress(user_id)
    if not user_data:
        await query.message.edit_text("❌ No progress data found. Use /start to begin!")
        return
    
    total_lessons = get_total_lessons()
    completed = get_completed_lessons(user_id)
    current = get_current_lesson(user_id)
    progress_pct = calculate_overall_progress(user_id, total_lessons)
    
    progress_text = f"""
📊 **Your Progress**

Current Lesson: {current}
Completed Lessons: {len(completed)}/{total_lessons}
Overall Progress: {progress_pct}%

{'🎓 Keep up the great work!' if len(completed) > 0 else '📚 Start your first lesson to begin!'}
    """
    
    keyboard = [
        [InlineKeyboardButton("📚 Continue Learning", callback_data="continue_lesson")],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(progress_text, reply_markup=reply_markup, parse_mode="Markdown")


async def show_all_lessons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show all available lessons."""
    query = update.callback_query
    
    titles = get_all_lesson_titles()
    lessons_text = "📋 **All Available Lessons:**\n\n" + "\n".join(titles)
    
    keyboard = [
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(lessons_text, reply_markup=reply_markup, parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    if data == "menu":
        await menu(update, context)
    elif data == "continue_lesson":
        current_lesson = get_current_lesson(user_id)
        await show_lesson(update, context, current_lesson)
    elif data == "show_progress":
        await show_progress(update, context)
    elif data == "all_lessons":
        await show_all_lessons(update, context)
    elif data.startswith("lesson_"):
        lesson_id = int(data.split("_")[1])
        await show_lesson(update, context, lesson_id)
    elif data.startswith("quiz_"):
        lesson_id = int(data.split("_")[1])
        await start_quiz(update, context, lesson_id)
    elif data.startswith("answer_"):
        answer_idx = int(data.split("_")[1])
        await handle_answer(update, context, answer_idx)


async def lesson_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /lesson command."""
    user_id = update.effective_user.id
    current_lesson = get_current_lesson(user_id)
    
    keyboard = [
        [InlineKeyboardButton("📚 Start Lesson", callback_data=f"lesson_{current_lesson}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Ready to start Lesson {current_lesson}?",
        reply_markup=reply_markup
    )


def main() -> None:
    """Start the bot."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token or token == "your_bot_token_here":
        logger.error("Please set TELEGRAM_BOT_TOKEN in .env file")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("lesson", lesson_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
