import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import setup_db,db_drop_and_create_all, Category, Question
from unittest.mock import patch 
load_dotenv()
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test=True)
        self.client = self.app.test_client
        self.database_name = os.getenv("DATABASE_NAME")
        HOST_NAME = os.getenv("DATABASE_HOST")
        USER_NAME = os.getenv("DATABASE_USER")
        PASSWORD  = os.getenv("DATABASE_PASSWORD")
        self.database_path ="postgresql://{}:{}@{}/{}".format(USER_NAME, PASSWORD,HOST_NAME, self.database_name)
        setup_db(app=self.app, database_path=self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_get_paginated_questions_bad_req(self):
        res = self.client().get('/questions?page=9000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('categories' in data)
        self.assertTrue(isinstance(data['categories'], dict))
    
    def test_get_categories_bad_req(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        
    def test_delete_question_bad_req(self):
        res = self.client().delete('/questions/xx')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
     
    def test_get_questions_by_keyword(self):
        data_with_searchTerm = {
            'searchTerm': 'Palace'
        }
        res = self.client().post('/questions', json = data_with_searchTerm)
        data = json.loads(res.data)

        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('categories' in data)
        self.assertTrue('currentCategory' in data)
    
    def test_get_questions_by_keyword_bad_req(self):
        data_with_searchTerm = {
            'searchTerm': '******'
        }
        res = self.client().post('/questions', json = data_with_searchTerm)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        

    def test_create_question(self):
        res = self.client().post('/questions', json = {
            'question' : 'alo alo',
            'answer' : '123',
            'category' : 1,
            'difficulty' : 2
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions'])) 
        
    def test_create_question_bad_req(self):
        res = self.client().post('/questions', json = {
            'question' : 'alo alo',
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_questions_by_categories(self):
        res = self.client().get( '/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
    
    def test_get_questions_by_categories_bad_req(self):
        res = self.client().get( '/categories/xx/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_quizzes(self):
        res = self.client().post('/quizzes', json = {
            'quiz_category': {'type': 'Science', 'id': 1},
            'previous_questions': []
        })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('total_questions' in data)
    
    def test_get_questions_by_quizzes_bad_req(self):
        res = self.client().post('/quizzes', json = {
            'previous_questions': []
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
     
    def test_not_found_error_handler(self):
        res = self.client().get('/nonexistent-endpoint')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_unprocessable_error_handler(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_bad_request_error_handler(self):
        question_id = 99999999999999
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_method_not_allowed_error_handler(self):
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()