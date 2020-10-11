# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import dateutil.parser
from datetime import datetime
from models import *
# ----------------------------------------------------------------------------#
# Supporting functions.
# ----------------------------------------------------------------------------#
# Get all tasks


def get_tasks():
    tasks = Task.query.order_by('id').all()
    formmated_tasks = [task.format() for task in tasks]
    return formmated_tasks


# Get all tasks for a selected user
def get_user_tasks(user_id):
    person = Person.query.filter(Person.id == user_id).one_or_none()
    if person is None:
        abort(404)

    formmated_tasks = [task.format() for task in person.tasks]
    return formmated_tasks


# Get all people
def get_people():
    people = Person.query.order_by('id').all()
    formmated_people = [person.format() for person in people]
    return formmated_people


# Find person
def taskLookup(description):
    return Task.query.filter_by(description=description).one_or_none()


# Find person
def personLookup(name, ssn):
    return Person.query.filter_by(name=name).filter_by(ssn=ssn).one_or_none()
