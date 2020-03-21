import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import pdb


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(question_data, page=1):
    """
    Chunks a list of question data into appropriately sized chunks.

    Parameters:
    page (int): Requested questions page
    question_data (list): List of question objects

    Returns:
    list: List of dictionaries containing question data
    """

    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in question_data]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    """Creates the flask app object and sets configs."""

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response


    @app.route("/categories", methods=["GET"])
    def get_categories():
        """Get all categories formatted as {1: 'Science', 2: 'Geography', ...} """

        # Available categories based on questions
        available_category_ids = list([question.category for question in Question.query.all()])

        # Return only categories that have associated questions
        categories_raw = Category.query.filter(Category.id.in_(available_category_ids))
        categories_formatted = {}
        for category in categories_raw:
            categories_formatted[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": categories_formatted
        })


    @app.route("/questions", methods=["GET"])
    def get_questions():
        """
        Get all questions, paginated in groups of ten.
        total_questions is the number of questions beyond.
        """

        page = request.args.get('page', 1, type=int)

        # Questions
        questions = Question.query.all()
        paginated_questions = paginate(questions, page=page)

        # Available categories based on questions
        available_category_ids = list([question.category for question in Question.query.all()])

        # Return only categories that have associated questions
        categories_raw = Category.query.filter(Category.id.in_(available_category_ids))
        categories_formatted = {}
        for category in categories_raw:
            categories_formatted[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(questions),
            "categories": categories_formatted
        })


    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        """Delete request for a specific question."""

        try:
            # Delete question
            question = Question.query.get(id)
            question.delete()

            # Query existing questions
            questions = Question.query.all()
            paginated_questions = paginate(questions, page=1)

            return jsonify({
                "success": True,
                "deleted_question": question.id,
                "questions": paginated_questions
            })
        except Exception:
            abort(422)


    @app.route("/questions", methods=["POST"])
    def new_or_searched_question():
        """
        Searches or creates a new question.

        If searchTerm exists, then retrieve it's value and retrieve search
        result.

        If searchTerm doesn't exist, retrieve the data to build a new
        question instance in the database.
        """

        data = request.get_json()

        # Search questions
        search_term = data["searchTerm"] if  "searchTerm" in data.keys() else None
        if search_term:
            question_results = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            question_results_formatted = [question.format() for question in question_results]

            return jsonify({
                "questions": question_results_formatted,
                "total_questions": len(question_results_formatted)
            })

        # Submit new question
        else:
            question = data["question"]
            answer = data["answer"]
            difficulty = data["difficulty"]
            category = data["category"]
            new_question = Question(
                question = question,
                answer = answer,
                difficulty = difficulty,
                category = category
            )

            # Add to database
            try:
                new_question.insert()
                return jsonify({
                    "success": True
                })
            except Exception:
                abort(422)


    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_by_category(id):
        """Retrieve questions based on a given category."""

        try:
            questions = Question.query.filter(Question.category == id)
            paginated_questions = paginate(questions, 1)
            return jsonify({
                "sucess": True,
                "questions": paginated_questions,
                "total_questions": len(paginated_questions)
            })
        except Exception:
            abort(422)


    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
        """
        Fetches new questions based previous questions asked throughout the
        quiz game.
        """

        # Rrequest data
        data = request.get_json()
        previous_questions = data["previous_questions"]
        quiz_category = data["quiz_category"]

        # New quiz questions
        question_candidates = []

        # Return all categories
        if quiz_category["type"] == "all":
            for question in Question.query.all():
                if not question.id in previous_questions:
                    question_candidates.append(question.format())

        # Return filtered results
        else:
            for question in Question.query.filter(Question.category == quiz_category["id"]):
                if not question.id in previous_questions:
                    question_candidates.append(question.format())

        # Return new quiz questions
        chosen_index = int(round(random.random() * len(question_candidates), 0))-1
        selected_question = question_candidates[chosen_index] if len(question_candidates)>0 else None
        return jsonify({
            "success": True,
            "question": selected_question
        })


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


    return app
