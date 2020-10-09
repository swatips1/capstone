#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
#
# import json
import dateutil.parser
# import babel
# from flask_babel import Babel
from datetime import datetime
#Import all models
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

# def format_datetime(value, format='medium'):
#   date = dateutil.parser.parse(value)
#   if format == 'full':
#       format="EEEE MMMM, d, y 'at' h:mma"
#   elif format == 'medium':
#       format="EE MM, dd, y h:mma"
#   return babel.dates.format_datetime(date, format)

# app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Supporting functions.
#----------------------------------------------------------------------------#
#Get all tasks
def get_tasks():
    tasks = Task.query.order_by('id').all()
    formmated_tasks = [task.format() for task in tasks]
    return formmated_tasks

#Get all tasks for a selected user
def get_user_tasks(user_id):
    person = Person.query.filter(Person.id == user_id).one_or_none()
    if person is None:
        abort(404)

    formmated_tasks = [task.format() for task in person.tasks]
    return formmated_tasks

#Get all people
def get_people():
    people = Person.query.order_by('id').all()
    formmated_people = [person.format() for person in people]
    return formmated_people

# Find person
def taskLookup(description):
    return Task.query.filter_by(description=description).one_or_none()

# Find person
def personLookup(name,ssn):
    return Person.query.filter_by(name=name).filter_by(ssn=ssn).one_or_none()
