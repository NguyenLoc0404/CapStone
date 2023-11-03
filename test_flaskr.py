import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import setup_db,db_drop_and_create_all, Category, Question
from unittest.mock import patch 
load_dotenv()

cilent_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0NTM0MDdjNDAzZGRlNmEyNWYzMzEiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5OTMzOTEsImV4cCI6MTY5OTA3OTc5MSwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzLWNhdGVnb3J5X2lkLXF1ZXN0aW9ucyIsInBhdGNoOnF1aXp6ZXMiLCJwb3N0OnF1ZXN0aW9ucyJdfQ.NoNvpHaagzTGdGTOsvgY_x2I_yzKWxlrN_RWSuZco9F6aiZJhBozywbaSO3Vampic3c2_eeaB3FOlHkrabEWV6u51pBPMc8qG2Xaz668nqGvFsiLY_RPE7s8igmNP5nsByCnMiQIFOw6zjLAjul70_3HOG44kLpwu-w6U_OnUIHVpKMDQqw-_PbXqU_OiTprt3g9F4vD_wCX1BTPry3yh-IcRGV3BaLSbz5CDDW25fKBusD_1xD2PxMZUvY0h3VZLAz_h4fDXgNujGo_oNeh3T35CLYWukfq2a0kbW9ZkNpokC7k2yHRMCueNQoTTLwxNcOIdWvVSTE_AC5es_aHAA'
}

employee_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0MDIzMWNiYTJmZWEyNjE4ZTMzZDIiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5OTM0MzYsImV4cCI6MTY5OTA3OTgzNiwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpxdWVzdGlvbnMiLCJnZXQ6Y2F0ZWdvcmllcy1jYXRlZ29yeV9pZC1xdWVzdGlvbnMiLCJwYXRjaDpxdWl6emVzIiwicG9zdDpxdWVzdGlvbnMiXX0.gwb5dX9G94Qbxkjk5xgxOclLo4KBmP0cujwpfeVr7Kla9V8QFJRKRIc152C3e7L7Tl_3wWGQlIEdYMHeN0rBiF-Y8GlhLU7N8jIDu127sgw7XeYk__ZpWT-0LLSpOIAk5wJkkjo8JbCOvT6NpBxJJuLhe-THm8eSVhbgOIoE_dODzkaC7cLaJu-IsqfOgSKB00CIjw0B8nicF9q-u2FwfGJPgQj82u-6vRbvk07RC82tykMkLMx4QVuU0ipIOr_bz3Uko8K-qV-oe1kkCPLwJEYKcE2P3LXsJGpf6GUGvHdOn8oW7M1jSUY08tP-n7PhTitl-d-rWWqYTriqeIes4w'
}

token_exprice_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0MDFhYzdjNDAzZGRlNmEyNWFlMTkiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5NjA1MjUsImV4cCI6MTY5ODk2NzcyNSwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzLWNhdGVnb3J5X2lkLXF1ZXN0aW9ucyIsInBhdGNoOnF1aXp6ZXMiLCJwb3N0OnF1ZXN0aW9ucyJdfQ.hnPCsLdyvTL4qHIOjDP9RuiVnjpkCWyK_oDIODDjzRHH0N8MrY4EzarLdkUAZcGU1J_f3YinS95jAFLdTaaJ6xI0TVbFQI2e_YAdgMXkyr4DgDCI1Wxy4VOuN1Vqfvsi3PoV6tM8sfWT9_CD9CRDBp5IbIxitAti0YxMw6Iv9dLI--RgI9MkNeH0kiYEjRgqS8CvQkLuAU4MMxhYb0PB2nSbb8Z_8It3Lo4v8FgtekMzgYgDTei7Eif3QCcy7PN2FevZwAN-eILyI8b3ZTKGiOBA-AIvSnjPKh0ASIbOoJMOkOgwvjK7aTfErXaTedZ3l5eBDsGE1XE3q4Qc8B75jA'
}
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
        res = self.client().delete('/questions/4',headers=employee_auth_header)
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
        res = self.client().post('/questions', json = data_with_searchTerm,headers=employee_auth_header)
        data = json.loads(res.data)

        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
        self.assertTrue('categories' in data)
        self.assertTrue('currentCategory' in data)
       

    def test_create_question(self):
        res = self.client().post('/questions', json = {
            'question' : 'alo alo',
            'answer' : '123',
            'category' : 1,
            'difficulty' : 2
        },headers=cilent_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions'])) 
           
    def test_get_questions_by_categories_with_token_exprice(self):
        res = self.client().get( '/categories/1/questions',headers=token_exprice_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token expired.')

    def test_get_questions_by_categories(self):
        res = self.client().get( '/categories/1/questions',headers=cilent_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('questions' in data)
        self.assertTrue('total_questions' in data)
    
    def test_get_questions_by_categories_bad_req(self):
        res = self.client().get( '/categories/xx/questions',headers=cilent_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_quizzes(self):
        res = self.client().patch('/quizzes', json = {
            'quiz_category': {'type': 'Science', 'id': 1},
            'previous_questions': []
        },headers=employee_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('total_questions' in data)
     
    def test_not_found_error_handler(self):
        res = self.client().get('/nonexistent-endpoint')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_dont_have_token(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'Authorization header is expected.')

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