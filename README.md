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
With Postgres running, create database of your choice using
```bash
createdb <db name>
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

Endpoint            Methods  Rule
------------------  -------  ------------------------------
add_person          POST     /people
add_task            POST     /tasks
assign_task         POST     /people/assign_task
delete_person       DELETE   /people/<int:person_id>/delete
delete_task         DELETE   /tasks/<int:task_id>/delete
find_person         POST     /people/find
find_task           POST     /tasks/find
hello               GET      /
people              GET      /people
static              GET      /static/<path:filename>
tasks               GET      /tasks
update_task_status  PATCH    /people/update_task_status
user_tasks          POST     /people/<int:user_id>/tasks

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

## Testing
To run the tests, run
```
dropdb choremonsta_test
createdb choremonsta_test
source setup.sh
python test_app.py
```
