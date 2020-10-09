import os
from flask import Flask, request, abort, jsonify, flash, current_app, redirect, url_for

from models import setup_db
# import babel
# from flask_babel import Babel
from flask_cors import CORS
from flask_cors import cross_origin
import json

#Authentication
from auth.auth import AuthError, requires_auth

#Import all models
from models import *

#Supporting functions
from lib import *

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app) #Basic use


    # app.jinja_env.filters['datetime'] = format_datetime
    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Routes
    '''

    '''
    -----------------------------------------------------------
    Default endpoint.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: None
    Expected Output: jsonified message.
    ***********************************************************
    -----------------------------------------------------------
    Linked tests:None
    -----------------------------------------------------------
    '''

    @app.route('/')
    def hello():
        return jsonify({'message': 'Welcome to Choremosta- World''s best chore organizer!'})

    '''
    -----------------------------------------------------------
    This endpoint to handles GET requests for all tasks
    for all people.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: None
    Expected Output:
         list of all tasks from database when successful.
         total number of tasks
         Error otherwise.
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: list_all_tasks
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_list_all_tasks
    -----------------------------------------------------------
    '''
    @app.route('/tasks', methods=['GET'])
    @requires_auth('list_all_tasks')
    def tasks(payload):
        try:
            tasks = get_tasks()
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message': e})
        return jsonify({'success': True,
                        'tasks' : tasks,
                        'totalTasks' : len(tasks)})

    '''
    -----------------------------------------------------------
    This endpoint to handles GET requests to get list of all
    people
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: None
    Expected Output:
         list of all peope from database when successful.
         total number of people
         Error otherwise.
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: list_all_people
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_list_all_people
    -----------------------------------------------------------
    '''
    @app.route('/people', methods=['GET'])
    @requires_auth('list_all_people')
    def people(payload):
        try:
            people = get_people()
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message': e})
        return jsonify({'success': True,
                        'people' : people,
                        'totalPeople' : len(people)})

    '''
    -----------------------------------------------------------
    This endpoint handles creation of new tasks via POST
    It returns list of all tasks from database.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
      description: string. Task description
    Expected Output:
      list of all tasks from database
      total number of tasks in the database
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: add_task
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_add_task, test_delete_task,
                 test_assign_task, test_list_user_taskss
    -----------------------------------------------------------
    '''
    @app.route('/tasks', methods=['POST'])
    @requires_auth('add_task')
    def add_task(payload):
      # try:
      description = request.get_json()['description']
      task = taskLookup(description)
      if task is not None:
          # return jsonify({'message': 'Tasks already exists. Please correct description and try again'})
          abort(422)
      task = Task(description=description)
      task.insert()
      return redirect(url_for('tasks'))

    '''
    -----------------------------------------------------------
    This endpoint handles creation of new person via POST
    It returns list of all people from database.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
      name: string. First and last name of the user,
                    separated by comma
      name: ssn.  ssn. Name and SSN together uniquely
                    Identify a person.
    Expected Output:
      list of all people from database
      total number of people in the database
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: add_person
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_add_task, test_delete_task,
                 test_assign_task, test_list_user_taskss
    -----------------------------------------------------------
    '''
    @app.route('/people', methods=['POST'])
    @requires_auth('add_person')
    def add_person(payload):
      try:
        name = request.get_json()['name']
        ssn = request.get_json()['ssn']
        person = Person(name=name, ssn=ssn)
        person.insert()
      except Exception as e:
          print(e)
          return jsonify({'message': e})
      return redirect(url_for('people'))

    '''
    -----------------------------------------------------------
    This endpoint to handles POST requests to assign task to
    person
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
        personId: int. Id of the person to whom the task is
                       being assigned.
        taskId: int. Id of the task being assigned to the user.
        startDate: datetime. Expected start date of the task.
        dueBy: datetime. Date by when the task is need to be
                         completed.
        status: string. Current state of the tasks.
    Expected Output:
         list of all tasks from database when successful.
         Error otherwise.
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: assign_task
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_assign_task, test_list_user_tasks
    -----------------------------------------------------------
    '''
    @app.route('/people/assign_task', methods=['POST'])
    @requires_auth('assign_task')
    def assign_task(payload):
        try:
            personId = request.get_json()['personId']
            taskId = request.get_json()['taskId']
            startDate = request.get_json()['startDate']
            dueBy = request.get_json()['dueBy']
            status = request.get_json()['status']
            personTask = PersonTask(personid=personId, taskid=taskId, startdate=startDate,
                                    dueby=dueBy, status=status)
            personTask.insert()
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message': e})
        return redirect(url_for('tasks'))

    '''
    -----------------------------------------------------------
    This endpoint to handles PATCH requests for tasks.
    It updates the status of the task with the new status.
    It returns list of all tasks from database.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
        personId: int. Id of the person to whose task is being
                       updated.
        taskId: int. Id of the task being updated.
        startDate: datetime. Expected start date of the task.
        status: string. Updated state of the tasks.
    Expected Output:
      list of all tasks from database
      total number of tasks
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: update_task_status
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_update_task_status
    -----------------------------------------------------------
    '''
    @app.route('/people/update_task_status', methods=['PATCH'])
    @requires_auth('update_task_status')
    def update_task_status(payload):
        personId = request.get_json()['personId']
        taskId = request.get_json()['taskId']
        startDate = request.get_json()['startDate']
        status = request.get_json()['status']

        personTask = PersonTask.query.filter(PersonTask.personid==personId, PersonTask.taskid==taskId,
                                             PersonTask.startdate==startDate
                                             ).one_or_none()
        # print(personTask)
        if personTask is None:
            abort(404)
        personTask.status = status
        personTask.update()
        tasks = get_tasks()
        return jsonify({'success': True,
                        'tasks' : tasks,
                        'totalTasks' : len(tasks)})

    '''
    -----------------------------------------------------------
    This endpoint to handles GET requests for all tasks
    for selected user id
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: id of the user
    Expected Output:
         list of all tasks from database when successful.
         Error otherwise.
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: list_user_tasks
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_list_user_tasks
    -----------------------------------------------------------
    '''
    @app.route('/people/<int:user_id>/tasks', methods=['POST'])
    @requires_auth('list_user_tasks')
    def user_tasks(payload, user_id):
        try:
            tasks = get_user_tasks(user_id)
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message': e})
        return jsonify({'success': True,
                        'user': user_id,
                        'user_tasks' : tasks})

    '''
    -----------------------------------------------------------
    This endpoint to handles DELETE requests for tasks.
    It returns list of all remaining tasks from database.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: id of the task
    Expected Output:
      list of all tasks from database
      total number of tasks
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: delete_task
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_del_task
    -----------------------------------------------------------
    '''
    @app.route('/tasks/<int:task_id>/delete', methods=['DELETE'])
    @requires_auth('delete_task')
    def delete_task(payload, task_id):
        task = Task.query.filter(Task.id == task_id).one_or_none()
        if task is None:
            abort(404)
        try:
            task.delete()
            tasks =get_tasks()
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message' : 'error'})
        return jsonify({'success': True,
                        'tasks' : tasks,
                        'totalTasks' : len(tasks)})

    '''
    -----------------------------------------------------------
    This endpoint to handles DELETE requests for people.
    It returns list of all remaining people from database.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs: id of the person
    Expected Output:
      list of all people from database
      total number of tasks
    ***********************************************************
    -----------------------------------------------------------
    Required Permissions: delete_person
    -----------------------------------------------------------
    -----------------------------------------------------------
    Linked tests:test_del_person
    -----------------------------------------------------------
    '''
    @app.route('/people/<int:person_id>/delete', methods=['DELETE'])
    @requires_auth('delete_person')
    def delete_person(payload, person_id):
        person = Person.query.filter(Person.id == person_id).one_or_none()
        if person is None:
            abort(404)
        try:
            person.delete()
            people =get_people()
        except Exception as e:
            print(e)
            return jsonify({'success': False,
                            'message' : 'error'})
        return jsonify({'success': True,
                        'people' : people,
                        'totalPeople' : len(people)})

    '''
    ***********************************************************
    Error Handler
    ***********************************************************
    '''
    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
               "success": False,
               "error": 500,
               "message": "internal server error"
           }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                 "success": False,
                 "error": 422,
                 "message": "unprocessable"
             }), 422

    @app.errorhandler(404)
    def not_found(error):
          return jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }), 404

    @app.errorhandler(400)
    def bad_request(error):
          return jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }), 400

    @app.errorhandler(AuthError)
    def not_authorized(AuthError):
        return jsonify({
              "success": False,
              "error": AuthError.status_code,
              "message": AuthError.error['code']
          }), 401

    '''
    ***********************************************************
    -----------------------------------------------------------
    Supporting routes. Used for testing. Not directly
    connected to use cases.
    -----------------------------------------------------------
    '''

    '''
    -----------------------------------------------------------
    This endpoint handles searching a task with specific
    description
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
      description: String. Task description.
    Expected Output:
      id of the task with matching description.
    ***********************************************************
    -----------------------------------------------------------
    Linked tests:test_find_person
    -----------------------------------------------------------
    '''
    @app.route('/tasks/find', methods=['POST'])
    def find_task():
        description = request.get_json()['description']
        task = taskLookup(description)
        if task is None:
            abort(404)
        return jsonify({'success': True,
                        'id' : task.id})

    '''
    -----------------------------------------------------------
    This endpoint handles searching a person with specific
    name and ssn.
    -----------------------------------------------------------
    ***********************************************************
    Expected Inputs:
      name: String. Name of the person.
      ssn: String. SSN of the person.
    Expected Output:
      id of the person with matching information.
    ***********************************************************
    -----------------------------------------------------------
    Linked tests:test_find_person
    -----------------------------------------------------------
    '''
    @app.route('/people/find', methods=['POST'])
    def find_person():
        name = request.get_json()['name']
        ssn = request.get_json()['ssn']
        person = personLookup(name, ssn)
        if person is None:
            abort(404)
        return jsonify({'success': True,
                        'id' : person.id})

    '''***********************************************************
    '''


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
