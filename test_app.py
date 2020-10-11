import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import *
from datetime import datetime, timedelta

db_name = 'choremosta_test'


class ChoremostaTestCase(unittest.TestCase):
    """This class represents Choremosta test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "choremosta_test"
        self.database_url = "postgres:Aspen100@localhost:5432"
        self.database_path = "postgresql://{}/{}".format(
            self.database_url, self.database_name)
        setup_db(self.app, self.database_path)

        # Permissions setUp
        self.child_user = os.getenv('child_user')
        self.parent_user = os.getenv('parent_user')

        # People related variables
        self.new_person = {
            'name': 'a, b',
            'ssn': '1000000000000000000000000000000'
            }

        self.new_person_for_assign = {
            'name': 'p, q',
            'ssn': '10000000000000sds00000000000000000'
            }

        self.new_person_for_delete = {
            'name': 'z, x',
            'ssn': '12345'
            }

        self.new_person_for_update = {
            'name': 'aa, bb',
            'ssn': '12345sss'
            }

        self.new_person_for_user_list = {
            'name': 'aaa, bbb',
            'ssn': '12345ssssssss'
            }
        # Task related variables

        self.new_task = {
            'description': 'I am brand new task'
            }

        self.new_task_for_assign = {
            'description': 'I am task for assignment'
            }

        self.new_task_for_delete = {
            'description': 'I am task for delete'
            }

        self.new_task_for_update = {
            'description': 'I am task for update'
            }

        self.new_task_for_user_list = {
            'description': 'I am task for user list'
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """ Begin Test Suit """

    # ************************************************************************************#
    # Tasks:Parent
    # ************************************************************************************#
    # ------------------------------------------------------------------------------------#
    # Add: Success
    # ------------------------------------------------------------------------------------#
    def test_add_task(self):
        """Test Add Task """
        print('..................Parent:Test Add Task.................')
        res = self.client().post(
            '/tasks', json=self.new_task,
            headers=[
                        ('Content-Type', 'application/json'),
                        ('Authorization', f'Bearer {self.parent_user}')
                    ],
            follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ------------------------------------------------------------------------------------#
    # Get: Success
    # ------------------------------------------------------------------------------------#
    def test_list_all_tasks(self):
        """Test List All Tasks """
        print('.............Parent:Test List All Tasks............')
        res = self.client().get(
                '/tasks',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ------------------------------------------------------------------------------------#
    # Delete task Success
    # ------------------------------------------------------------------------------------#
    def test_delete_task(self):
        """Test Delete Task"""
        print('................Parent:Test Delete Task..................')

        # Create the task as the parent since child
        # doesnt have the right to do so
        res = self.client().post(
                '/tasks', json=self.new_task_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    # ------------------------------------------------------------------------------------#
    # Assign Tasks: Success
    # ------------------------------------------------------------------------------------#
    def test_assign_task(self):
        """Test assign task """
        print('..................Parent:Test Assign Task....................')
        res = self.client().post(
                '/people', json=self.new_person_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_assign
                )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': datetime.now(),
            'dueBy': datetime.now() + timedelta(days=10),
            'status': 'Pending'
            }

        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

    # ------------------------------------------------------------------------------------#
    # Update task status: Success
    # ------------------------------------------------------------------------------------#
    def test_update_task_status(self):
        """Test update task status """
        print('..............Parent:Test update of task status..............')
        res = self.client().post(
                '/people', json=self.new_person_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': date,
            'dueBy': datetime.now() + timedelta(days=10),
            'status': 'Pending'
            }

        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        self.updated_assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': date,
            'status': 'Started'
            }

        res = self.client().patch(
                '/people/update_task_status', json=self.updated_assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

    # ------------------------------------------------------------------------------------#
    # Get list of all tasks for a user: Success
    #  ------------------------------------------------------------------------------------#
    def test_list_user_tasks(self):
        """Test list of all task for user """
        print('...............Parent:Test list tasks for user................')

        res = self.client().post(
                '/people', json=self.new_person_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': datetime.now(),
            'dueBy': datetime.now() + timedelta(days=10),
            'status': 'Pending'
            }

        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/people/' + str(person_id) + '/tasks',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['user_tasks'], True)

        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

    # #************************************************************************************#
    # # People:Parent
    # #************************************************************************************#
    # ------------------------------------------------------------------------------------#
    # Add: Success
    # ------------------------------------------------------------------------------------#
    def test_add_person(self):
        """Test Add Person """
        print('..................Parent:Test Add Person..................')
        res = self.client().post(
                '/people', json=self.new_person,
                headers=[
                        ('Content-Type', 'application/json'),
                        ('Authorization', f'Bearer {self.parent_user}')
                    ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ------------------------------------------------------------------------------------#
    # Get: Success
    # ------------------------------------------------------------------------------------#
    def test_list_all_people(self):
        """Test List All People"""
        print('..............Parent:Test List all People.................')
        res = self.client().get(
                '/people',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ------------------------------------------------------------------------------------#
    # Delete person Success
    # ------------------------------------------------------------------------------------#
    def test_delete_person(self):
        """Test Delete Person"""
        print('.............Parent:Test Delete Person...............')

        res = self.client().post(
                '/people', json=self.new_person_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_delete
                        )
        data = json.loads(res.data)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    # ************************************************************************************#
    # Tasks:Child
    # ************************************************************************************#
    # ------------------------------------------------------------------------------------#
    # Add: Success
    # ------------------------------------------------------------------------------------#
    def test_child_add_task(self):
        """Test Add Task """
        print('.................Child:Test Add Task................')
        res = self.client().post(
            '/tasks', json=self.new_task,
            headers=[
                        ('Content-Type', 'application/json'),
                        ('Authorization', f'Bearer {self.child_user}')
                    ],
            follow_redirects=True)
        self.assertEqual(res.status_code, 401)

    # ------------------------------------------------------------------------------------#
    # Get: Success
    # ------------------------------------------------------------------------------------#
    def test_child_list_all_tasks(self):
        """Test List All Tasks """
        print('...............Child:Test List All Tasks................')
        res = self.client().get(
                '/tasks',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ])
        self.assertEqual(res.status_code, 401)

    # #************************************************************************************#
    # # People
    # #************************************************************************************#
    # ------------------------------------------------------------------------------------#
    # Add: Success
    # ------------------------------------------------------------------------------------#
    def test_child_add_person(self):
        """Test Add Person """
        print('...................Child:Test Add Person..................')
        res = self.client().post(
                '/people', json=self.new_person,
                headers=[
                        ('Content-Type', 'application/json'),
                        ('Authorization', f'Bearer {self.child_user}')
                    ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # ------------------------------------------------------------------------------------#
    #  Get: Success
    # ------------------------------------------------------------------------------------#
    def test_child_list_all_people(self):
        """Test List All People"""
        print('.................Child:Test List all People..................')
        res = self.client().get(
                '/people',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    # ------------------------------------------------------------------------------------#
    # Delete task Success
    # ------------------------------------------------------------------------------------#
    def test_child_delete_task(self):
        """Test Delete Task"""
        print('.................Child:Test Delete Task................')
        # Need to ask task to delete as parent
        res = self.client().post(
                '/tasks', json=self.new_task_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        # Attempt delete as child
        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ])
        self.assertEqual(res.status_code, 401)

        # Clean as parent
        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

    # ------------------------------------------------------------------------------------#
    # Delete person Success
    # ------------------------------------------------------------------------------------#
    def test_child_delete_person(self):
        """Test Delete Person"""
        print('.................Child:Test Delete Person.................')
        # Need to ask task to delete as parent
        res = self.client().post(
                '/people', json=self.new_person_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_delete,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        person_id = json.loads(res.data).get('id', None)

        # Attempt delete as child
        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ])
        self.assertEqual(res.status_code, 401)

        # Clean as parent
        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

    # ------------------------------------------------------------------------------------#
    # Assign Tasks: Success
    # ------------------------------------------------------------------------------------#
    def test_child_assign_task(self):
        """Test assign task """
        print('.................Child:Test Assign Task..................')
        # Need to ask task to delete as parent
        res = self.client().post(
                '/people', json=self.new_person_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_assign,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': date,
            'dueBy': date,
            'status': 'Pending'
            }

        # Child:Attempt assignment
        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 401)

        # Cleanup as parent
        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

    # ------------------------------------------------------------------------------------#
    # Update task status: Success
    # ------------------------------------------------------------------------------------#
    def test_child_update_task_status(self):
        """Test update task status """
        print('................Child:Test update of task status..............')
        res = self.client().post(
                '/people', json=self.new_person_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_update,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': date,
            'dueBy': date,
            'status': 'Pending'
            }

        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        self.updated_assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': date,
            'status': 'Started'
            }

        # Child:Attempt update
        res = self.client().patch(
                '/people/update_task_status', json=self.updated_assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ], follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        # Cleanup as parent
        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

    # ------------------------------------------------------------------------------------#
    # Get list of all tasks for a user: Success
    # ------------------------------------------------------------------------------------#
    def test_child_list_user_tasks(self):
        """Test list of all task for user """
        print('................Child:Test list tasks for user................')
        # Need to ask task to delete as parent
        res = self.client().post(
                '/people', json=self.new_person_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalPeople'], True)

        res = self.client().post(
                '/people/find', json=self.new_person_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        person_id = json.loads(res.data).get('id', None)

        res = self.client().post(
                '/tasks', json=self.new_task_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalTasks'], True)

        res = self.client().post(
                '/tasks/find', json=self.new_task_for_user_list,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        data = json.loads(res.data)
        task_id = json.loads(res.data).get('id', None)

        self.assignment = {
            'personId': person_id,
            'taskId': task_id,
            'startDate': datetime.now(),
            'dueBy': datetime.now() + timedelta(days=10),
            'status': 'Pending'
            }

        res = self.client().post(
                '/people/assign_task', json=self.assignment,
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ], follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['totalTasks'], True)

        # Child: Attempt getting list of tasks for user
        res = self.client().post(
                '/people/' + str(person_id) + '/tasks',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.child_user}')
                        ])
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['user_tasks'], True)

        # Cleanup as parent
        res = self.client().delete(
                '/people/' + str(person_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(
                '/tasks/' + str(task_id) + '/delete',
                headers=[
                            ('Content-Type', 'application/json'),
                            ('Authorization', f'Bearer {self.parent_user}')
                        ])
        self.assertEqual(res.status_code, 200)


#
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
