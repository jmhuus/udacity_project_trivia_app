import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

import pdb


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
                'localhost:5432',
                self.database_name
            )
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
    Write at least one test for each test for successful operation and for
    expected errors.
    """
    def test_categories_get(self):
        get_response = self.client().get("/categories")
        data = json.loads(get_response.data)
        self.assertEqual(get_response.status_code, 200)
        self.assertGreater(len(data["categories"].keys()), 0)


    def test_questions_get(self):
        get_response = self.client().get("/questions")
        data = json.loads(get_response.data)
        self.assertEqual(get_response.status_code, 200)
        self.assertGreater(data["total_questions"], 0)
        self.assertGreater(len(data["questions"]), 0)
        self.assertEqual(data["success"], True)

    def test_question_delete(self):
        # Add a question to be deleted
        new_question_data = {
            "question": "Will this test pass?",
            "answer": "yes",
            "difficulty": 1,
            "category": 1
        }
        create_question_response = self.client().post(
                "/questions",
                json=new_question_data
            )
        data = json.loads(create_question_response.data)
        new_question_id = data["new_question_id"]
        self.assertEqual(data["success"], True)
        self.assertNotEqual(new_question_id, None)

        # Delete the newly created question
        delete_question_response = self.client().delete(
                f"/questions/{new_question_id}"
            )
        data = json.loads(delete_question_response.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_question"], new_question_id)

    def test_question_create(self):
        # Add a question
        new_question_data = {
            "question": "Will this test pass?",
            "answer": "yes",
            "difficulty": 1,
            "category": 1
        }
        create_question_response = self.client().post(
                "/questions",
                json=new_question_data
            )
        data = json.loads(create_question_response.data)
        new_question_id = data["new_question_id"]
        self.assertEqual(data["success"], True)
        self.assertNotEqual(new_question_id, None)


    def test_question_search(self):
        # Add a question to be searched
        new_question_data = {
            "question": "New question to search for.... CAT?",
            "answer": "yes",
            "difficulty": 1,
            "category": 1
        }
        create_question_response = self.client().post(
                "/questions",
                json=new_question_data
            )
        data = json.loads(create_question_response.data)
        new_question_id = data["new_question_id"]
        self.assertEqual(data["success"], True)
        self.assertNotEqual(new_question_id, None)

        # Search for the newly created question
        search_question_data = {
            "searchTerm": "cat"
        }
        search_question_response = self.client().post(
                "/questions",
                json=search_question_data
            )
        data = json.loads(search_question_response.data)
        self.assertGreater(len(data["questions"]), 0)
        self.assertGreater(data["total_questions"], 0)


    def test_question_by_category_get(self):
        # Add a question to be searched
        chosen_category = 5
        new_question_data = {
            "question": "Will this test pass?",
            "answer": "yes",
            "difficulty": 1,
            "category": chosen_category
        }
        create_question_response = self.client().post(
                "/questions",
                json=new_question_data
            )
        data = json.loads(create_question_response.data)
        new_question_id = data["new_question_id"]
        self.assertEqual(data["success"], True)
        self.assertNotEqual(new_question_id, None)

        # Search for questions by category
        questions_by_category_response = self.client().get(
                f"/categories/{chosen_category}/questions"
            )
        data = json.loads(questions_by_category_response.data)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(data["questions"]), 0)
        self.assertGreater(data["total_questions"], 0)


    def test_play_game(self):
        quiz_category = 1
        quiz_question_count = 0
        quiz_params = {
            "previous_questions": [],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }

        # Loop through questions until the quiz is over
        while True:
            question_response = self.client().post("/quizzes", json=quiz_params)
            data = json.loads(question_response.data)
            returned_question = data["question"]

            self.assertEqual(question_response.status_code, 200)
            if returned_question:
                self.assertTrue(data["question"]["id"] not in quiz_params["previous_questions"])
                quiz_params["previous_questions"].append(data["question"]["id"])

            # Exit condition
            if returned_question == None:
                break






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
