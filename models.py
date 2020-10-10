import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have name
# and type ( c for child or p for parent)
'''


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ssn = db.Column(db.String, nullable=False)
    db.UniqueConstraint('name', 'ssn', name='uq_person')

    tasks = db.relationship("PersonTask", cascade="all, delete")

    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name}

    def __repr__(self):
        return f'<I am a Person. My Id is: {self.id},my name is {self.name}>'


'''
Tasks
Have description
'''


class Task(db.Model):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    db.UniqueConstraint('description', name='uq_task')

    personTasks = db.relationship("PersonTask", cascade="all, delete")

    def __init__(self, description):
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'description': self.description}


'''
PersonTask
Bind person to task(s). Have start date, due date and status
'''


class PersonTask(db.Model):
    __tablename__ = 'persontasks'
    dt = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    personid = db.Column(db.Integer, db.ForeignKey('person.id', name ='fk_person_task_person'), primary_key=True, nullable=False)
    taskid = db.Column(db.Integer, db.ForeignKey('task.id', name ='fk_person_task_task'), primary_key=True, nullable=False)
    startdate = db.Column(db.DateTime, nullable=False, primary_key=True,  default=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))
    dueby = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))
    status = Column(String, nullable=False, default='Not_Started')

    def __init__(self, personid, taskid, startdate, dueby, status):
        self.personid = personid
        self.taskid = taskid
        self.startdate = startdate
        self.dueby = dueby
        self.status = status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'personId': self.personid,
          'taskId': self.taskid,
          'startDate': self.startdate,
          'dueBy': self.dueby,
          'status': self.status
          }
