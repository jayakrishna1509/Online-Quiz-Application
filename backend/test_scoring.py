import pytest
import json
from app import app, db
from models import Quiz, Question, Option

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            setup_test_data()
        yield client
        
    with app.app_context():
        db.drop_all()

def setup_test_data():
    """Setup test quiz data"""
    # Create a test quiz
    quiz = Quiz(title="Test Quiz")
    db.session.add(quiz)
    db.session.flush()
    
    # Add questions
    q1 = Question(text="What is 2 + 2?", quiz_id=quiz.id)
    db.session.add(q1)
    db.session.flush()
    
    # Add options for question 1
    Option(text="3", is_correct=False, question_id=q1.id)
    Option(text="4", is_correct=True, question_id=q1.id)
    Option(text="5", is_correct=False, question_id=q1.id)
    Option(text="6", is_correct=False, question_id=q1.id)
    
    q2 = Question(text="What is the capital of France?", quiz_id=quiz.id)
    db.session.add(q2)
    db.session.flush()
    
    # Add options for question 2
    Option(text="London", is_correct=False, question_id=q2.id)
    Option(text="Paris", is_correct=True, question_id=q2.id)
    Option(text="Berlin", is_correct=False, question_id=q2.id)
    Option(text="Madrid", is_correct=False, question_id=q2.id)
    
    q3 = Question(text="What is 10 / 2?", quiz_id=quiz.id)
    db.session.add(q3)
    db.session.flush()
    
    # Add options for question 3
    Option(text="3", is_correct=False, question_id=q3.id)
    Option(text="4", is_correct=False, question_id=q3.id)
    Option(text="5", is_correct=True, question_id=q3.id)
    Option(text="6", is_correct=False, question_id=q3.id)
    
    db.session.commit()

def test_all_correct_answers(client):
    """Test scoring with all correct answers"""
    # Get quiz and questions
    response = client.get('/api/quizzes/1/questions')
    assert response.status_code == 200
    questions = json.loads(response.data)
    
    # Submit all correct answers
    answers = [
        {"questionId": questions[0]['id'], "selectedOptionId": questions[0]['options'][1]['id']},  # 4
        {"questionId": questions[1]['id'], "selectedOptionId": questions[1]['options'][1]['id']},  # Paris
        {"questionId": questions[2]['id'], "selectedOptionId": questions[2]['options'][2]['id']}   # 5
    ]
    
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['score'] == 3
    assert result['total'] == 3
    assert result['percentage'] == 100.0

def test_all_wrong_answers(client):
    """Test scoring with all wrong answers"""
    response = client.get('/api/quizzes/1/questions')
    assert response.status_code == 200
    questions = json.loads(response.data)
    
    # Submit all wrong answers
    answers = [
        {"questionId": questions[0]['id'], "selectedOptionId": questions[0]['options'][0]['id']},  # 3
        {"questionId": questions[1]['id'], "selectedOptionId": questions[1]['options'][0]['id']},  # London
        {"questionId": questions[2]['id'], "selectedOptionId": questions[2]['options'][0]['id']}   # 3
    ]
    
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['score'] == 0
    assert result['total'] == 3
    assert result['percentage'] == 0.0

def test_partial_correct_answers(client):
    """Test scoring with some correct and some wrong answers"""
    response = client.get('/api/quizzes/1/questions')
    assert response.status_code == 200
    questions = json.loads(response.data)
    
    # Submit mixed answers (2 correct, 1 wrong)
    answers = [
        {"questionId": questions[0]['id'], "selectedOptionId": questions[0]['options'][1]['id']},  # 4 (correct)
        {"questionId": questions[1]['id'], "selectedOptionId": questions[1]['options'][0]['id']},  # London (wrong)
        {"questionId": questions[2]['id'], "selectedOptionId": questions[2]['options'][2]['id']}   # 5 (correct)
    ]
    
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['score'] == 2
    assert result['total'] == 3
    assert result['percentage'] == 66.67

def test_missing_answers(client):
    """Test scoring with missing answers"""
    response = client.get('/api/quizzes/1/questions')
    assert response.status_code == 200
    questions = json.loads(response.data)
    
    # Submit only 2 answers out of 3
    answers = [
        {"questionId": questions[0]['id'], "selectedOptionId": questions[0]['options'][1]['id']},  # 4 (correct)
        {"questionId": questions[1]['id'], "selectedOptionId": questions[1]['options'][1]['id']}   # Paris (correct)
    ]
    
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['score'] == 2
    assert result['total'] == 3
    assert result['percentage'] == 66.67

def test_results_details(client):
    """Test that results include detailed information"""
    response = client.get('/api/quizzes/1/questions')
    assert response.status_code == 200
    questions = json.loads(response.data)
    
    answers = [
        {"questionId": questions[0]['id'], "selectedOptionId": questions[0]['options'][1]['id']}
    ]
    
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    
    # Check that results array exists and has correct structure
    assert 'results' in result
    assert len(result['results']) == 3
    
    for res in result['results']:
        assert 'questionId' in res
        assert 'questionText' in res
        assert 'userAnswer' in res
        assert 'correctAnswer' in res
        assert 'isCorrect' in res

def test_invalid_quiz_id(client):
    """Test submitting answers for non-existent quiz"""
    answers = [{"questionId": 1, "selectedOptionId": 1}]
    
    response = client.post('/api/quizzes/999/submit',
                          data=json.dumps({'answers': answers}),
                          content_type='application/json')
    
    assert response.status_code == 404

def test_missing_answers_field(client):
    """Test submitting without answers field"""
    response = client.post('/api/quizzes/1/submit',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
