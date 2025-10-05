import json
import os
from app import app, db
from models import Quiz, Question, Option

def load_quiz_data_from_json(json_file='quiz_data.json'):
    """Load quiz data from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), json_file)
    
    if not os.path.exists(json_path):
        print(f"Warning: {json_file} not found. Using default data.")
        return get_default_quiz_data()
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return get_default_quiz_data()

def get_default_quiz_data():
    """Return default quiz data if JSON file is not available"""
    return {
        "quizzes": [
            {
                "title": "Programming Fundamentals",
                "questions": [
                    {
                        "text": "What does HTML stand for?",
                        "options": [
                            {"text": "Hyper Text Markup Language", "is_correct": True},
                            {"text": "High Tech Modern Language", "is_correct": False},
                            {"text": "Home Tool Markup Language", "is_correct": False},
                            {"text": "Hyperlinks and Text Markup Language", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Which programming language is known as the 'language of the web'?",
                        "options": [
                            {"text": "Python", "is_correct": False},
                            {"text": "JavaScript", "is_correct": True},
                            {"text": "Java", "is_correct": False},
                            {"text": "C++", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What is the purpose of CSS?",
                        "options": [
                            {"text": "To structure web pages", "is_correct": False},
                            {"text": "To style web pages", "is_correct": True},
                            {"text": "To add interactivity", "is_correct": False},
                            {"text": "To manage databases", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Which symbol is used for single-line comments in Python?",
                        "options": [
                            {"text": "//", "is_correct": False},
                            {"text": "#", "is_correct": True},
                            {"text": "/*", "is_correct": False},
                            {"text": "--", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What does API stand for?",
                        "options": [
                            {"text": "Application Programming Interface", "is_correct": True},
                            {"text": "Advanced Programming Integration", "is_correct": False},
                            {"text": "Automated Program Interaction", "is_correct": False},
                            {"text": "Application Process Integration", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "JavaScript Basics",
                "questions": [
                    {
                        "text": "Which keyword is used to declare a variable in JavaScript?",
                        "options": [
                            {"text": "var", "is_correct": True},
                            {"text": "int", "is_correct": False},
                            {"text": "string", "is_correct": False},
                            {"text": "define", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What method is used to add an element to the end of an array?",
                        "options": [
                            {"text": "append()", "is_correct": False},
                            {"text": "push()", "is_correct": True},
                            {"text": "add()", "is_correct": False},
                            {"text": "insert()", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Which operator is used for strict equality in JavaScript?",
                        "options": [
                            {"text": "==", "is_correct": False},
                            {"text": "===", "is_correct": True},
                            {"text": "=", "is_correct": False},
                            {"text": "!=", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What does 'NaN' stand for?",
                        "options": [
                            {"text": "Not a Number", "is_correct": True},
                            {"text": "Null and None", "is_correct": False},
                            {"text": "New Array Node", "is_correct": False},
                            {"text": "Negative and Null", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Database Concepts",
                "questions": [
                    {
                        "text": "What does SQL stand for?",
                        "options": [
                            {"text": "Structured Query Language", "is_correct": True},
                            {"text": "Simple Question Language", "is_correct": False},
                            {"text": "Standard Query Logic", "is_correct": False},
                            {"text": "System Query Language", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Which SQL command is used to retrieve data from a database?",
                        "options": [
                            {"text": "GET", "is_correct": False},
                            {"text": "FETCH", "is_correct": False},
                            {"text": "SELECT", "is_correct": True},
                            {"text": "RETRIEVE", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What is a primary key?",
                        "options": [
                            {"text": "A unique identifier for a record", "is_correct": True},
                            {"text": "The first column in a table", "is_correct": False},
                            {"text": "A password for the database", "is_correct": False},
                            {"text": "The main table in a database", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "General Knowledge",
                "questions": [
                    {
                        "text": "What is the capital of France?",
                        "options": [
                            {"text": "London", "is_correct": False},
                            {"text": "Berlin", "is_correct": False},
                            {"text": "Paris", "is_correct": True},
                            {"text": "Madrid", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Which planet is known as the Red Planet?",
                        "options": [
                            {"text": "Venus", "is_correct": False},
                            {"text": "Mars", "is_correct": True},
                            {"text": "Jupiter", "is_correct": False},
                            {"text": "Saturn", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Who painted the Mona Lisa?",
                        "options": [
                            {"text": "Vincent van Gogh", "is_correct": False},
                            {"text": "Pablo Picasso", "is_correct": False},
                            {"text": "Leonardo da Vinci", "is_correct": True},
                            {"text": "Michelangelo", "is_correct": False}
                        ]
                    },
                    {
                        "text": "What is the largest ocean on Earth?",
                        "options": [
                            {"text": "Atlantic Ocean", "is_correct": False},
                            {"text": "Indian Ocean", "is_correct": False},
                            {"text": "Arctic Ocean", "is_correct": False},
                            {"text": "Pacific Ocean", "is_correct": True}
                        ]
                    },
                    {
                        "text": "In which year did World War II end?",
                        "options": [
                            {"text": "1943", "is_correct": False},
                            {"text": "1945", "is_correct": True},
                            {"text": "1947", "is_correct": False},
                            {"text": "1950", "is_correct": False}
                        ]
                    }
                ]
            }
        ]
    }

def initialize_database():
    """Initialize database with quiz data"""
    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating new tables...")
        db.create_all()
        
        # Load quiz data
        print("Loading quiz data...")
        quiz_data = load_quiz_data_from_json()
        
        # Add quizzes to database
        for quiz_info in quiz_data['quizzes']:
            print(f"\nAdding quiz: {quiz_info['title']}")
            quiz = Quiz(title=quiz_info['title'])
            db.session.add(quiz)
            db.session.flush()  # Get the quiz ID
            
            for question_info in quiz_info['questions']:
                question = Question(
                    text=question_info['text'],
                    quiz_id=quiz.id
                )
                db.session.add(question)
                db.session.flush()  # Get the question ID
                
                for option_info in question_info['options']:
                    option = Option(
                        text=option_info['text'],
                        is_correct=option_info['is_correct'],
                        question_id=question.id
                    )
                    db.session.add(option)
                
                print(f"  - Added question: {question_info['text'][:50]}...")
        
        # Commit all changes
        db.session.commit()
        print("\n✓ Database initialized successfully!")
        
        # Display summary
        total_quizzes = Quiz.query.count()
        total_questions = Question.query.count()
        total_options = Option.query.count()
        
        print(f"\nDatabase Summary:")
        print(f"  - Total Quizzes: {total_quizzes}")
        print(f"  - Total Questions: {total_questions}")
        print(f"  - Total Options: {total_options}")

if __name__ == '__main__':
    initialize_database()
