"""
Educational content structure for the Telegram bot.
Contains lessons with videos, texts, and quizzes.
"""

lessons = [
    {
        "id": 1,
        "title": "Introduction to Programming",
        "video_url": "https://www.youtube.com/watch?v=example1",
        "text": """
Welcome to your first programming lesson!

Programming is the art of giving instructions to computers. In this lesson, you'll learn:
- What is programming?
- Why learn programming?
- Basic programming concepts
- How computers understand code

Programming languages are tools that help us communicate with computers. Just like human languages, 
they have their own syntax and rules. Don't worry - we'll start simple and build up from there!
        """,
        "quiz": [
            {
                "question": "What is programming?",
                "options": [
                    "Writing instructions for computers",
                    "Playing computer games",
                    "Browsing the internet",
                    "Typing on a keyboard"
                ],
                "correct_answer": 0
            },
            {
                "question": "Which of these is a programming language?",
                "options": [
                    "English",
                    "Python",
                    "Microsoft Word",
                    "Google Chrome"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": 2,
        "title": "Variables and Data Types",
        "video_url": "https://www.youtube.com/watch?v=example2",
        "text": """
Variables: Storing Information

In programming, variables are like containers that store data. Think of them as labeled boxes 
where you can put different types of information.

Common Data Types:
- Strings: Text data (e.g., "Hello World")
- Numbers: Integers (1, 2, 3) and Floats (3.14, 2.5)
- Booleans: True or False values
- Lists: Collections of items

Example:
name = "Alice"  # String variable
age = 25        # Integer variable
is_student = True  # Boolean variable

Variables make programs dynamic and flexible!
        """,
        "quiz": [
            {
                "question": "What is a variable?",
                "options": [
                    "A fixed value that never changes",
                    "A container for storing data",
                    "A type of computer",
                    "A programming error"
                ],
                "correct_answer": 1
            },
            {
                "question": "Which data type represents True/False values?",
                "options": [
                    "String",
                    "Integer",
                    "Boolean",
                    "Float"
                ],
                "correct_answer": 2
            }
        ]
    },
    {
        "id": 3,
        "title": "Control Structures: If Statements",
        "video_url": "https://www.youtube.com/watch?v=example3",
        "text": """
Making Decisions in Code

Control structures allow your program to make decisions. The if statement is like asking a question:
"If this condition is true, do this action."

Basic Syntax:
if condition:
    # do something
else:
    # do something else

Example:
age = 18
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

You can also use elif for multiple conditions:
if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")
        """,
        "quiz": [
            {
                "question": "What does an if statement do?",
                "options": [
                    "Stores data in variables",
                    "Makes decisions based on conditions",
                    "Repeats code multiple times",
                    "Defines a function"
                ],
                "correct_answer": 1
            },
            {
                "question": "What keyword is used for additional conditions?",
                "options": [
                    "else if",
                    "elif",
                    "elseif",
                    "otherwise"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": 4,
        "title": "Loops: Repeating Actions",
        "video_url": "https://www.youtube.com/watch?v=example4",
        "text": """
Loops: Automating Repetitive Tasks

Loops allow you to repeat code multiple times without writing it over and over.

For Loop:
Used when you know how many times to repeat:
for i in range(5):
    print(i)  # Prints 0, 1, 2, 3, 4

While Loop:
Used when you want to repeat until a condition is false:
count = 0
while count < 5:
    print(count)
    count += 1

Loops are powerful tools for processing collections of data and automating repetitive tasks!
        """,
        "quiz": [
            {
                "question": "What is the purpose of a loop?",
                "options": [
                    "To make decisions",
                    "To repeat code multiple times",
                    "To store data",
                    "To end a program"
                ],
                "correct_answer": 1
            },
            {
                "question": "Which loop is used when you know the exact number of repetitions?",
                "options": [
                    "while loop",
                    "for loop",
                    "if loop",
                    "repeat loop"
                ],
                "correct_answer": 1
            }
        ]
    },
    {
        "id": 5,
        "title": "Functions: Organizing Your Code",
        "video_url": "https://www.youtube.com/watch?v=example5",
        "text": """
Functions: Reusable Blocks of Code

Functions are like mini-programs within your program. They help you organize code and avoid repetition.

Defining a Function:
def greet(name):
    return f"Hello, {name}!"

# Using the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!

Benefits of Functions:
- Code reusability
- Better organization
- Easier testing and debugging
- Makes code more readable

Parameters allow you to pass data into functions, and return statements send data back!
        """,
        "quiz": [
            {
                "question": "What is a function?",
                "options": [
                    "A type of variable",
                    "A reusable block of code",
                    "A loop structure",
                    "A data type"
                ],
                "correct_answer": 1
            },
            {
                "question": "What keyword is used to send data back from a function?",
                "options": [
                    "send",
                    "give",
                    "return",
                    "output"
                ],
                "correct_answer": 2
            }
        ]
    }
]

def get_lesson_by_id(lesson_id):
    """Get a specific lesson by its ID."""
    for lesson in lessons:
        if lesson["id"] == lesson_id:
            return lesson
    return None

def get_total_lessons():
    """Get the total number of lessons."""
    return len(lessons)

def get_all_lesson_titles():
    """Get a list of all lesson titles."""
    return [f"{lesson['id']}. {lesson['title']}" for lesson in lessons]
