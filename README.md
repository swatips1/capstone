# Full Stack Choremonsta API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependenciesby running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
#TODO: How will the database be setup ??
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Alternatively, you could execute setup.sh to set all variables:

```bash
source setup.sh
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

TODO: Need to update this section.
```
Below is list of all Endpoints:

Endpoints
*** Categories***
GET '/categories'
POST '/categories'
POST '/categories/<int:category_id>/questions'

*** Questions***
GET '/questions'
POST '/questions'
POST '/questions/search'
DELETE '/questions/<int:question_id>/delete'

*** Both***
POST '/quizzes'

*** Categories***
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

POST '/categories'
- Creates a new category.
- Request Arguments:
    type: String. Name of the new category.
- Returns: int: id of the newly created category.

POST '/categories/<int:category_id>/questions'
- Searches for all questions based on category id provided.  
- Request Arguments: Int: id of the category.
- Returns: A list of objects, questions that belong to selected category, that contains object with structure
           {question (string), answer (string), difficulty (int) and category(int)}
[{answer: "The Palace of Versailles", category: 3, difficulty: 3, question: "In which royal palace would you find the Hall of Mirrors?" },
 {answer: "Lake Victoria", category: 3, difficulty: 2, question:"What is the largest lake in Africa?"}  
]

*** Questions***
GET '/questions'
- Fetches a list of questions.
- Request Arguments: None
- Returns: A list of objects, questions, with object structure {question (string), answer (string), difficulty (int) and category(int)}
[{answer: "The Palace of Versailles", category: 3, difficulty: 3, question: "In which royal palace would you find the Hall of Mirrors?" },
 {answer: "Lake Victoria", category: 3, difficulty: 2, question:"What is the largest lake in Africa?"}  
]

POST '/questions'
- Creates a new question.
- Request Arguments:
    question: string. The text of the question
    answer: string. The text of the answer
    difficulty: int. Range is 1-5.
    category: id of the category the question belongs to. Mapped to id from categories table in the database.
- Returns: A list of objects, questions, with object structure {question (string), answer (string), difficulty (int) and category(int)}
[{answer: "The Palace of Versailles", category: 3, difficulty: 3, question: "In which royal palace would you find the Hall of Mirrors?" },
 {answer: "Lake Victoria", category: 3, difficulty: 2, question:"What is the largest lake in Africa?"}  
]

POST '/questions/search'
- Searches for all questions based on partial search term. The search term is compared with Question's question field.  
- Request Arguments: String: Partial or entire string to search.
- Returns: A list of objects, questions, that contains object with structure {question (string), answer (string), difficulty (int) and category(int)}
[{answer: "The Palace of Versailles", category: 3, difficulty: 3, question: "In which royal palace would you find the Hall of Mirrors?" },
 {answer: "Lake Victoria", category: 3, difficulty: 2, question:"What is the largest lake in Africa?"}  
]

DELETE '/questions/<int:question_id>/delete'
- Deletes selected question.
- Request Arguments: Int: question_id of the question
- Returns: A list of objects, questions, that contains object with structure {question (string), answer (string), difficulty (int) and category(int)}
[{answer: "The Palace of Versailles", category: 3, difficulty: 3, question: "In which royal palace would you find the Hall of Mirrors?" },
 {answer: "Lake Victoria", category: 3, difficulty: 2, question:"What is the largest lake in Africa?"}  
]

*** Both***
POST '/quizzes'
-  This endpoint generates questions to play the quiz. It takes category and previous question parameters and returns a random questions within the
  given category, if provided, and that is not one of the previous questions.  
- Request Arguments:
    quiz_category: Object. The category user clicked to play the quiz
    previous_questions: Object. List of id(s) of previously answered questions
- Returns: An objects, question,  with structure {question (string), answer (string), difficulty (int) and category(int)}
           List of ids of previously answered questions
{"previous_questions": [10],
 "question":{ answer: "Uruguay", category: 6, difficulty: 4, question:"Which country won the first ever soccer World Cup in 1930?"}
}
```

## Testing
To run the tests, run
```
dropdb choremonsta_test
createdb choremonsta_test
<!-- psql trivia_test < trivia.psql -->
python test_app.py
```
