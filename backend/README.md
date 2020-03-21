# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

**DONE** We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

**DONE** Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

**DONE** ```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
**DONE** With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server
**DONE** From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. **DONE** Use Flask-CORS to enable cross-domain requests and set response headers.
2. **DONE** Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. **DONE** Create an endpoint to handle GET requests for all available categories.
4. **DONE** Create an endpoint to DELETE question using a question ID.
5. **DONE** Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. **DONE** Create a GET endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. **DONE** Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. **DONE** Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
# Endpoints Guide

### URL
https://triviagame.com/

### Methods

##### Fetch all question categories:
Retrieve all question categories and their corresponding ID.

Method: `GET`

Route: `/categories`

Response:
```
{
  'categories': {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography',
    '4': 'History',
    '6': 'Sports'
  },
  'success': true
}
```

<br/>
<br/>

##### Fetch all questions:
Get all questions, paginated in groups of ten.
total_questions is the number of questions beyond. *This endpoint is not used to play the quiz game! See /quizzes.*

Method: `GET`

Route: `/questions`

Response:
```
{
  'categories': {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography',
    '4': 'History',
    '6': 'Sports'
  },
  'questions': [
    {
      'answer': 'Uruguay',
      'category': 6,
      'difficulty': 4,
      'id': 11,
      'question': 'Which country...?'
    }, ...],
  'success': true,
  'total_questions' 16
}
```

<br/>
<br/>

##### Remove a question:
Delete request for a specific question.

Method: `DELETE`

Route: `/questions/<int:id>`

Response:
```
{
    'success': True,
    'deleted_question': 27,
    'questions': [
        {
            'id': 11,
            'question':
            'Which country won...?',
            'answer': 'Uruguay',
            'category': 6,
            'difficulty': 4
        }, ...]
}
```

<br/>
<br/>

##### Search/create a question:
If searchTerm exists, an array of questions will be returned where the substring matches the question. If searchTerm doesn't exist, a new question object will be added to the database based on the provided data.

Method: `POST`

Route: `/questions`

> **Request Arguments**
>
> * **searchTerm** OPTIONAL - use searchTerm to search for questions with the matching substring. Omit `searchTerm` if creating a new question.
```
{
    'searchTerm': 'mars'
}
```
>
> *or*
> * **question** - question to be stored and available during the trivia game.
> * **answer** - answer to the corresponding question.
> * **difficulty** - 5 hard, 1 easy
> * **category** - question category ID.
```
{
    'question': 'How many... Mars?',
    'answer': '21 months',
    'difficulty': '3',
    'category': 1
}
```


Search Response:
```
{
  "questions": [
    {
      "answer": "Top Gun",
      "category": 2,
      "difficulty": 1,
      "id": 24,
      "question": "Which movie are characters Mavrick and Goose in?"
    }
  ],
  "total_questions": 1
}
```
Create New Question Response:
```
{'success': True}
```

<br/>
<br/>

##### Fetch questions by category:
Retrieve questions based on a given category ID.

Method: `GET`

Route: `/categories/<int:id>/questions`

Response:
```
{
    'sucess': True,
    'questions': [
        {
            'id': 16,
            'question': 'Which Dutch graphic...?',
            'answer': 'Escher',
            'category': 2,
            'difficulty': 1
        }, ...]    
     'total_questions': 5
}
```

<br/>
<br/>

##### Play the quiz:
Fetches new questions based previous questions asked throughout the quiz game.

Method: *POST*

Route: */quizzes*

> ***Request Arguments***
* **previous_questions** - an array of question IDs previously asked. These will be filtered out in subsequent questions.
* **quiz_category** - object of the current category. Contains *type* and *id*.
```
{
    'previous_questions': [22, 20, ...],
    'quiz_category': {
        'type': 'Science',
        'id': '1'
        }
}
```


# Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
