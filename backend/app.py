from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_app, db
from models import Quiz, Question, Option
import json
import os

# --- App Initialization ---
app = Flask(__name__)
CORS(app)

# --- Database Initialization ---
init_app(app)

# --- API Routes ---

@app.route('/api/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz"""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_quiz = Quiz(title=data['title'])
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({'id': new_quiz.id, 'title': new_quiz.title}), 201

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    """Get all available quizzes"""
    try:
        all_quizzes = Quiz.query.all()
        quizzes_list = [{'id': quiz.id, 'title': quiz.title} for quiz in all_quizzes]
        return jsonify(quizzes_list)
    except Exception as e:
        print(f"Error fetching quizzes: {e}")
        return jsonify({'error': 'Failed to fetch quizzes'}), 500

@app.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz by ID"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        return jsonify({'id': quiz.id, 'title': quiz.title})
    except Exception as e:
        print(f"Error fetching quiz {quiz_id}: {e}")
        return jsonify({'error': 'Quiz not found'}), 404

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
def add_question_to_quiz(quiz_id):
    """Add a question to a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    if not data or 'text' not in data or 'options' not in data:
        return jsonify({'error': 'Missing text or options'}), 400
    
    # Validate question text length (300 character limit)
    if len(data['text']) > 300:
        return jsonify({'error': 'Question text must be 300 characters or less'}), 400
    
    # Validate that exactly one option is marked as correct
    correct_options = [opt for opt in data['options'] if opt.get('is_correct', False)]
    if len(correct_options) != 1:
        return jsonify({'error': 'Exactly one option must be marked as correct'}), 400
    
    new_question = Question(text=data['text'], quiz_id=quiz.id)
    for option_data in data['options']:
        new_option = Option(
            text=option_data['text'],
            is_correct=option_data.get('is_correct', False),
            question=new_question
        )
        db.session.add(new_option)
    
    db.session.add(new_question)
    db.session.commit()
    
    return jsonify({
        'message': 'Question added successfully',
        'question_id': new_question.id
    }), 201

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_questions_for_quiz(quiz_id):
    """Get all questions for a specific quiz (without correct answers)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        questions_list = []
        
        for question in quiz.questions:
            options_list = []
            for option in question.options:
                # Don't send is_correct to frontend
                options_list.append({
                    'id': option.id,
                    'text': option.text
                })
            
            questions_list.append({
                'id': question.id,
                'text': question.text,
                'options': options_list
            })
        
        return jsonify(questions_list)
    except Exception as e:
        print(f"Error fetching questions for quiz {quiz_id}: {e}")
        return jsonify({'error': 'Failed to fetch questions'}), 500

@app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    """Submit quiz answers and calculate score"""
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    
    if not data or 'answers' not in data:
        return jsonify({'error': 'Missing answers'}), 400
    
    user_answers = {
        answer['questionId']: answer['selectedOptionId'] 
        for answer in data['answers']
    }
    
    score = 0
    results = []
    questions = quiz.questions
    
    for question in questions:
        correct_option = next(
            (opt for opt in question.options if opt.is_correct),
            None
        )
        user_answer_id = user_answers.get(question.id)
        
        is_correct = False
        if correct_option and user_answer_id == correct_option.id:
            score += 1
            is_correct = True
        
        # Find the text of the user's answer and the correct answer
        user_answer_text = next(
            (opt.text for opt in question.options if opt.id == user_answer_id),
            "Not Answered"
        )
        correct_answer_text = correct_option.text if correct_option else "N/A"
        
        results.append({
            'questionId': question.id,
            'questionText': question.text,
            'userAnswer': user_answer_text,
            'correctAnswer': correct_answer_text,
            'isCorrect': is_correct
        })
    
    return jsonify({
        'score': score,
        'total': len(questions),
        'percentage': round((score / len(questions) * 100), 2) if len(questions) > 0 else 0,
        'results': results
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Quiz API is running'}), 200

# Create database tables when app starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
