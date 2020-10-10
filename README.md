# Full Stack Choremonsta API Backend

## About
The Choremonsta app is used to manage chores for a busy team such as a family.
A parent user can send a post request with description to create a new task.
They can send a post request with name and ssn to create a new person.
They can send get requests to get a list of all people / tasks.
They can send post request to assign task to a person.
They can send delete requests to delete task / person, with id corresponding in each case.

A child and parent user can send a post request to see all tasks assigned to them.
They can send a post request to update the status of their task.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

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

## API ARCHITECTURE AND TESTING
###Endpoint Library:

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of the user. Two roles are assigned to this API: 'Parent' and 'Child'.

Roles:
 Parent: Parent manages all aspects of chormonsta. They can add/delete person, add tasks, assign tasks to people and delete task. They can see a list of
         all tasks and people.
 Child:  Child can see tasks assigned to them and modify the status of their tasks.


Permissions associated with Parent:
add_person : Add new person					
add_task : Add new task						
assign_task : Assign task to person				
delete_person : Delete a person					
delete_task : Delete a task					
list_all_people : List all people					
list_all_tasks : List all tasks					
list_user_tasks : List all of tasks assigned to you			
update_task_status : Update status of a task			

Permissions associated with Child:
list_user_tasks : List all of tasks assigned to you
update_task_status : Update status of a task


Endpoint            Methods  Rule
------------------  -------  ------------------------------
hello               GET      /
people              GET      /people
tasks               GET      /tasks
add_person          POST     /people
add_task            POST     /tasks
assign_task         POST     /people/assign_task
user_tasks          POST     /people/<int:user_id>/tasks
delete_person       DELETE   /people/<int:person_id>/delete
delete_task         DELETE   /tasks/<int:task_id>/delete
update_task_status  PATCH    /people/update_task_status

#### GET '/hello'
Default path. Returns greeting.
Response output:
 {message	"Welcome to Choremosta- Worlds best chore organizer!"}

#### GET '/people'
Returns a list of people, with their id and first and last name separated by comma.
Sample response output:
{
    "people": [
        {
            "id": 1,
            "name": "p, 23"
        }
    ],
    "success": true,
    "totalPeople": 1
}


#### GET '/tasks'
Returns a list of people, with their id and description.
Sample response output:
{
    "success": true,
    "tasks": [
        {
            "description": "I am brand new task",
            "id": 1
        }
    ],
    "totalTasks": 1
}


#### POST '/add_person'
Creates a new person in the app. User is expected to provide unique combination of
first and last name of the user, separated by comman and the ssn of the user.
Returns a list of all people in the app.
Sample request:
{
    "name": "p, 23",
    "ssn": "100000000000200sds000000000000sdsd000002"
}
Sample response output:
{
    "people": [
        {
            "id": 1,
            "name": "p, 23"
        }
    ],
    "success": true,
    "totalPeople": 1
}


#### POST '/add_task'
Creates a new task in the app. User is expected to provide the description of the task.
Returns a list of all tasks in the app.
Sample request:
{
    "description": "I am brand new task"
}

Sample response output:
{
    "success": true,
    "tasks": [
        {
            "description": "I am brand new task",
            "id": 1
        }
    ],
    "totalTasks": 1
}


#### POST '/assign_task'
Assigns a task to a user. The user is expecter to provide id of the task, id of the person,
start date for the task, date by when the task is due to be completed and the current status of the task. Returns a list of all tasks in the app.
Sample request:
{
    "personId":1,
    "taskId": 1,
    "startDate": "2020-10-25",
    "dueBy":  "2020-10-25",
    "status": "Pending"
}

Sample response output:
{
    "success": true,
    "tasks": [
        {
            "description": "I am brand new task",
            "id": 1
        }
    ],
    "totalTasks": 1
}


#### POST '/user_tasks'
Returns all the tasks assigned to the selected user.
Sample request:
/people/<int:user_id>/tasks

Sample response output:
{
    "success": true,
    "user": 2,
    "user_tasks": [
        {
            "dueBy": "Sun, 25 Oct 2020 00:00:00 GMT",
            "personId": 2,
            "startDate": "Sun, 25 Oct 2020 00:00:00 GMT",
            "status": "Pending",
            "taskId": 2
        }
    ]
}

#### DELETE '/delete_person'
Deletes person associated with the provided id. Returns a list of rest of the people in the app.
Sample request:
{{host}}/people/1/delete

Sample response output:
{
    "people": [
        {
            "id": 2,
            "name": "p1, 23"
        }
    ],
    "success": true,
    "totalPeople": 1
}


#### DELETE '/delete_task'
Deletes tasks associated with the provided id. Returns a list of rest of the tasks in the app.
Sample request:
{{host}}/tasks/1/delete

Sample response output:
{
    "success": true,
    "tasks": [
        {
            "description": "I am brand new task1",
            "id": 2
        }
    ],
    "totalTasks": 1
}

#### PATCH '/update_task_status'
Updates task associated with the combined value of id of person, id of task, stare date and due date.
The status of the task is updated with the new status provided in the request.
Returns as list of all tasks in the app.
Sample request:
{
    "personId":1,
    "taskId": 1,
    "startDate": "2020-10-25",
    "dueBy":  "2020-10-25",
    "status": "Started"
}
Sample response output:
{
    "success": true,
    "tasks": [
        {
            "description": "I am brand new task",
            "id": 1
        }
    ],
    "totalTasks": 1
}

## Testing
To run the tests, run
```
dropdb choremonsta_test
createdb choremonsta_test
source setup.sh
python test_app.py
```

The application  can also be accessed via Heroku using the URL:
https://sskelly-udacity.herokuapp.com

## Testing
There are 18 unittests in test_app.py. To run this file use:
```
dropdb choremonsta_test
createdb choremonsta_test
python3 test_app.py
```
The tests include tests demonstrating role-based access control,
where all endpoints are tested with and without the correct authorization.
Further, the file 'chormosta.postman_collection.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> directory/chormosta.postman_collection.json
3. Click on the runner, select the collection and run all the tests.

## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'user' and 'seller' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL:
https://sskelly-udacity.herokuapp.com

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.
