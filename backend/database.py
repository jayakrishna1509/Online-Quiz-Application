from flask_sqlalchemy import SQLAlchemy
import os

# Create a SQLAlchemy instance
db = SQLAlchemy()

def init_app(app):
    """Initialize the database with the Flask app"""
    # Create instance folder if it doesn't exist
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "quiz.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize app with database
    db.init_app(app)
