from database import db

class Quiz(db.Model):
    """Quiz model representing a quiz"""
    __tablename__ = 'quiz'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Quiz {self.id}: {self.title}>'

class Question(db.Model):
    """Question model representing a quiz question"""
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Question {self.id}: {self.text[:50]}...>'

class Option(db.Model):
    """Option model representing an answer option for a question"""
    __tablename__ = 'option'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    def __repr__(self):
        return f'<Option {self.id}: {self.text[:30]}... (Correct: {self.is_correct})>'
