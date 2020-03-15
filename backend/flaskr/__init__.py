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
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route("/categories", methods=["GET"])
    def get_categories():

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


    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions (COMPLETE),
    number of total questions (COMPLETE), current category (PENDING),
    categories (PENDING).

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route("/questions", methods=["GET"])
    def get_questions():
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
            "categories": categories_formatted,
            "current_category": None # TODO(jordanhuus): find out what current_category is used for
        })



    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        pdb.set_trace()
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


    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route("/questions", methods=["POST"])
    def new_or_searched_question():
        data = request.get_json()

        # Search questions
        search_term = data["searchTerm"]
        if search_term:
            question_results = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            question_results_formatted = [question.format() for question in question_results]

            return jsonify({
                "questions": question_results_formatted,
                "total_questions": len(question_results_formatted),
                "current_category": None # TODO(jordanhuus): find out what current_category is used for
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


    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_by_category(id):
        try:
            questions = Question.query.filter(Question.category == id)
            paginated_questions = paginate(questions, 1)
            return jsonify({
                "sucess": True,
                "questions": paginated_questions,
                "current_category": id,
                "total_questions": len(paginated_questions)
            })
        except Exception:
            abort(422)


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_question():
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



    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
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
