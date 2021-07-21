import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

pg_port ="5432"
pg_user = "rubaa"
pg_pwd= "12345678"
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        #self.database_path = "postgresql:///{}".format(self.database_name)
        self.database_path = "postgresql://{username}:{password}@localhost:{port}/trivia_test".format(username=pg_user, password=pg_pwd, port=pg_port)
        setup_db(self.app, self.database_path)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
     #test get categories
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_non_exist_category_404(self):
        response = self.client().get('/categories/9999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #------------test get questions-----------------#
    #success
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #Fail
    def test_get_questions_404(self):
        response = self.client().get('/questions?page=2000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    #----------------------- test delete a question------------------#
    #success
    def test_delete_question(self):
        response = self.client().delete('/questions/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'],"2")
    #Fail
    def test_delete_question_404(self):
        response = self.client().delete('/questions/5000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)


    #--------test create question------------#
    #success
    def test_create_question(self):
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #Fail
    def test_create_question_422(self):
        new_question = {
            'question': 'Test question',
            'answer': 'Test answer',
            'category': 1
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    #--------- test search term ----------------#
    #success
    def test_search(self):
        response = self.client().post('/questions/search', json={'searchTerm': 'title'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #fail
    def test_search_fail(self):
        response = self.client().post('/questions/search', json={'searchTerm':'Ruba'})

        data = json.loads(response.data)

        self.assertEqual(data['total_questions'],0)
        self.assertEqual(data['success'], True)


    #-------test get questions by category-----------#
    #success
    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertEqual(data['success'], True)
    #fail
    def test_get_questions_by_category_404(self):
        response = self.client().get('/categories/a/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    #-----------test quiz-------------#
    #success
    def test_quiz(self):
        quiz_round = {'previous_questions': [], 'quiz_category': {'type': 'Geography', 'id': 14}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #fail
    def test_quiz_422(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
