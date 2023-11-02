import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import json
from logger import Logger

logger = Logger.get_logger(__name__)

database_path = os.getenv('DATA_URL')

if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    logger.info(f'Giá trị URL cơ sở dữ liệu: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    with app.app_context():
        db.init_app(app)
        db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
    
def db_drop_and_create_all():
    db.create_all()
    if Category.query.first() is None:
        insert_categories()
    if Question.query.first() is None:
        insert_questions()
 

def insert_categories():
    category_data = [
        'Science',
        'Art',
        'Geography',
        'History',
        'Entertainment',
        'Sports'
    ]
    for category in category_data:
        new_category = Category(type=category)
        new_category.insert()

def insert_questions():
    question_data = [
        ("Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "Maya Angelou", 4, 2),
        ("What boxer's original name is Cassius Clay?", "Muhammad Ali", 4, 1),
        ("What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", "Apollo 13", 5, 4),
        ( "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", "Tom Cruise", 5, 4),
        ("What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", "Edward Scissorhands", 5, 3),
        ("Which is the only team to play in every soccer World Cup tournament?", "Brazil", 6, 3),
        ("Which country won the first-ever soccer World Cup in 1930?", "Uruguay", 6, 4),
        ("Who invented Peanut Butter?", "George Washington Carver", 4, 2),
        ("What is the largest lake in Africa?", "Lake Victoria", 3, 2),
        ("In which royal palace would you find the Hall of Mirrors?", "The Palace of Versailles", 3, 3),
        ("The Taj Mahal is located in which Indian city?", "Agra", 3, 2),
        ("Which Dutch graphic artist–initials M C was a creator of optical illusions?", "Escher", 2, 1),
        ( "La Giaconda is better known as what?", "Mona Lisa", 2, 3),
        ("How many paintings did Van Gogh sell in his lifetime?", "One", 2, 4),
        ("Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?", "Jackson Pollock", 2, 2),
        ("What is the heaviest organ in the human body?", "The Liver", 1, 4),
        ("Who discovered penicillin?", "Alexander Fleming", 1, 3),
        ("Hematology is a branch of medicine involving the study of what?", "Blood", 1, 4),
        ("Which dung beetle was worshipped by the ancient Egyptians?", "Scarab", 4, 4)
    ]

    for question in question_data:
        new_question = Question(
            question=question[0],
            answer=question[1],
            category=question[2],
            difficulty=question[3],
        )
        new_question.insert()

