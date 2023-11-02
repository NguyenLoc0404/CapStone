import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import Integer
from models import db_drop_and_create_all, setup_db, Question, Category
from auth import AuthError, requires_auth, get_token_auth_header
from logger import Logger

logger = Logger.get_logger(__name__)

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test=False):
    # create and configure the app
    app = Flask(__name__)
    if not test:
        setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    app.route('/', methods=['GET']
              )(lambda: jsonify({'message': 'Hello Friend!'}))

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,selection)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({'success': True,
                        'questions': current_questions,
                        'total_questions': len(Question.query.all()),
                        'categories': formatted_categories,
                        'currentCategory': categories[0].id
                        })
    
    @app.route('/questions', methods=['POST'])
    def get_questions_by_keyword():
        body = request.get_json()
        searchTerm = body.get('searchTerm',None)

        if searchTerm is None:
            return create_question()

        questions = Question.query.filter(Question.question.ilike(f"%{searchTerm}%"))
        if questions is None:
            abort(404)
        current_questions = paginate_questions(request,questions)
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({'success': True,
                        'questions': current_questions,
                        'total_questions': len(current_questions),
                        'categories': formatted_categories,
                        'currentCategory': categories[0].id
                        })
    
    def create_question():
        body = request.get_json()
        new_question = body.get('question',None)
        new_answer = body.get('answer',None)
        new_category = body.get('category',None)
        new_difficulty = body.get('difficulty',None)
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request,selection)
            return jsonify({'success': True,
                            'created': question.id,
                            'questions': current_questions,
                            'total_questions': len(Question.query.all())
                            })
        except:
            abort(422)


    @app.route('/quizzes', methods=['POST'])
    @requires_auth('post:quizzes')
    def get_questions_by_quizzes():
        body = request.get_json()
        quiz_category = body.get('quiz_category',None)
        previous_questions = body.get('previous_questions',[])
        if quiz_category['id'] == 0:
            questions = Question.query.order_by(Question.id).all()
        else:
            questions = Question.query.filter(Question.category.cast(Integer) == quiz_category['id']).all()
            
        available_questions = [question.format() for question in questions]
        if questions is None:
            abort(404)
        
        if len(previous_questions) == 0:
            current_question = random.choice(available_questions)
        else:
            filtered_questions = [question for question in available_questions if question['id'] not in previous_questions]
            if len(filtered_questions) != 0:
                current_question = random.choice(filtered_questions)
            else:
                return jsonify({'success': True,
                        'total_questions': len(available_questions),
                        })

        return jsonify({'success': True,
                        'question': current_question,
                        'questions': available_questions,
                        'total_questions': len(available_questions),
                        })
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @requires_auth('delete:questions')
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,selection)
        return jsonify({'success': True,
                        'deleted': question_id,
                        'questions': current_questions,
                        'total_questions': len(current_questions)
                        })

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({'success': True,
                        'categories': formatted_categories
                        })
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @requires_auth('get:categories-category_id-questions')
    def get_questions_by_categories(category_id):
        questions = Question.query.filter(Question.category.cast(Integer) == int(category_id)).all()
        if questions is None:
            abort(404)
        current_questions = paginate_questions(request,questions)
        return jsonify({'success': True,
                        'questions': current_questions,
                        'total_questions': len(questions),
                        })
    

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app

app = create_app()
with app.app_context():
    db_drop_and_create_all()

if __name__ == '__main__':
    app.run()
