import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testdb"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_ques = {"question": "How Many", "answer": "5", "category": "6", "difficulty": "3"}
        self.new_ques_2 = {"question": "How Many", "answer": "5", "category": "45", "difficulty": "3"}
        self.new_ques_3 = {"question": "How Many", "answer": "5", "category": "45"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["categories"])

    def test_404_get_categories(self):
        res = self.client().get('/categorie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])

    def test_pagination_invalid_page(self):
        res = self.client().get('/questions?page=15')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_delete_questions(self):
        res = self.client().delete('/questions/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["deleted_question_id"])
        self.assertTrue(data["total_questions"])

    def test_delete_invalid_questions(self):
        res = self.client().delete('/questions/400')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_create_questions(self):
        res = self.client().post('/questions', json=self.new_ques)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["new question id"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_400_create_questions(self):
        res = self.client().post('/questions', json=self.new_ques_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_422_create_questions(self):
        res = self.client().post('/questions', json=self.new_ques_3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": 'which'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_404_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": '522'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_get_question_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["category_questions"])

    def test_404_get_question_by_category(self):
        res = self.client().get('/categories/652/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])

    def test_get_questions_to_play(self):
        res = self.client().post('/quizzes', json={"quiz_category": {"id": "4"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["question"])

    def test_400_get_questions_to_play(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data["message"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
