# Bernuhov-PRO
Educational Telegram Bot with Video Lessons, Texts, and Quizzes

## Overview

An interactive educational Telegram bot that guides users through a structured learning pipeline. The bot provides:
- 📹 **Video lessons** - Links to educational video content
- 📝 **Text content** - Detailed explanations and learning materials
- ❓ **Short quizzes** - Interactive quizzes to test knowledge
- 📊 **Progress tracking** - Automatic tracking of user progress through lessons

## Features

### Educational Pipeline
- **Automatic onboarding**: New users are automatically enrolled in the educational pipeline when they start the bot
- **Sequential learning**: Lessons are presented in a structured order
- **Progress tracking**: User progress is saved and can be resumed at any time
- **Interactive quizzes**: Each lesson includes quiz questions to reinforce learning
- **Score tracking**: Quiz scores are recorded for each lesson

### Current Curriculum
The bot includes 5 programming lessons:
1. Introduction to Programming
2. Variables and Data Types
3. Control Structures: If Statements
4. Loops: Repeating Actions
5. Functions: Organizing Your Code

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bernuhov/Bernuhov-PRO.git
cd Bernuhov-PRO
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Add your Telegram Bot Token to `.env`:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

To get a bot token:
- Message [@BotFather](https://t.me/botfather) on Telegram
- Use `/newbot` command to create a new bot
- Copy the token provided

## Usage

### Running the Bot

```bash
python bot.py
```

### Bot Commands

- `/start` - Start the bot and enroll in the educational pipeline
- `/menu` - Show the main menu with navigation options
- `/lesson` - Start or continue the current lesson

### User Journey

1. User starts the bot with `/start`
2. User is automatically enrolled in the educational pipeline
3. User can navigate through lessons using the menu
4. Each lesson includes:
   - A video link to watch
   - Text content to read
   - A quiz to complete
5. After completing a quiz, progress is saved and the user moves to the next lesson
6. Users can check their progress at any time

## Project Structure

```
Bernuhov-PRO/
├── bot.py              # Main bot application with handlers
├── lessons.py          # Educational content (videos, texts, quizzes)
├── user_progress.py    # User progress tracking system
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Adding New Lessons

To add new lessons, edit `lessons.py` and add a new lesson dictionary to the `lessons` list:

```python
{
    "id": 6,  # Next lesson ID
    "title": "Your Lesson Title",
    "video_url": "https://www.youtube.com/watch?v=...",
    "text": """
    Your lesson content here...
    """,
    "quiz": [
        {
            "question": "Your question?",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": 0  # Index of correct option (0-3)
        }
    ]
}
```

## Technical Details

### Dependencies
- `python-telegram-bot` (v20.7) - Telegram Bot API wrapper
- `python-dotenv` (v1.0.0) - Environment variable management
- `pyyaml` (v6.0.1) - YAML parsing support

### Data Storage
User progress is stored in `user_progress.json` (created automatically when the bot runs). This file tracks:
- Current lesson for each user
- Completed lessons
- Quiz scores
- Activity timestamps

## Development

### Testing
You can test the bot by:
1. Starting the bot locally
2. Opening Telegram and finding your bot
3. Sending `/start` to begin
4. Going through the educational pipeline

### Extending the Bot
The modular design makes it easy to:
- Add new lesson types
- Implement different quiz formats
- Add multimedia content
- Create branching learning paths
- Integrate with external learning platforms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
