# project/restful_api/views.py


import datetime

from functools import wraps
from flask import jsonify, Blueprint, session
from flask_restful import Resource, reqparse, abort, fields, marshal_with

from project import db, the_restful_api
from project.models import Task


################
#    config    #
################

restful_api_blueprint = Blueprint('restful_api', __name__)


##########################
#    helper functions    #
##########################

def abort_if_task_doesnt_exist(task_id):
    tasks = db.session.query(Task).all()
    task_exist = False
    for task in tasks:
        if task_id == task.task_id:
            task_exist = True
    if not task_exist:
        abort(404, message="Task {} doesn't exist".format(task_id))


# http://flask-restful.readthedocs.io/en/latest/quickstart.html#data-formatting
resource_fields = {
    'task_id': fields.Integer,
    'name': fields.String,
    'due_date': fields.DateTime(dt_format='iso8601'),
    'priority': fields.Integer,
    'posted_date': fields.DateTime(dt_format='iso8601'),
    'status': fields.Integer,
    'user_id': fields.Integer,
}


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            abort(401, message="Unauthorized")
    return wrap


class TaskDao(object):
    def __init__(self, task_id, name, due_date, priority, posted_date,
                 status, user_id):
        super(TaskDao, self).__init__()
        self.task_id = task_id
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.posted_date = posted_date
        self.status = status
        self.user_id = user_id

        # This field will not be sent in the response
        self.sensitive = 'some value'


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('due_date')
parser.add_argument('priority', type=int, help='Priority of the task')


######################
#    restful APIs    #
######################

class TaskAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        task = db.session.query(Task).filter_by(task_id=task_id).first()
        return TaskDao(task_id=task.task_id, name=task.name,
                       due_date=task.due_date, priority=task.priority,
                       posted_date=task.posted_date, status=task.status,
                       user_id=task.user_id), 200

    @login_required
    def delete(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        task = db.session.query(Task).filter_by(task_id=task_id)
        task.delete()
        db.session.commit()
        return '', 204

    # TODO Add PUT(update) method
    # TODO Change to only allow logged in users to update and delete task
    @login_required
    @marshal_with(resource_fields)
    def patch(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        task = db.session.query(Task).filter_by(task_id=task_id)
        task.update({"status": "0"})
        db.session.commit()
        task = task.first()
        return TaskDao(task_id=task.task_id, name=task.name,
                       due_date=task.due_date, priority=task.priority,
                       posted_date=task.posted_date, status=task.status,
                       user_id=task.user_id), 200


class TaskListAPI(Resource):
    def get(self):
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
            }
            json_results.append(data)
        return jsonify(items=json_results)

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        new_task = Task(
            args['name'],
            datetime.datetime.strptime(args['due_date'], '%m/%d/%Y'),
            args['priority'],
            datetime.datetime.utcnow(),
            '1',
            '1',
        )
        db.session.add(new_task)
        db.session.commit()
        result = TaskDao(task_id=new_task.task_id,
                         name=new_task.name,
                         due_date=new_task.due_date,
                         priority=new_task.priority,
                         posted_date=new_task.posted_date,
                         status=new_task.status,
                         user_id=new_task.user_id)
        return result, 201


the_restful_api.add_resource(TaskListAPI, '/api/v2/tasks/')
the_restful_api.add_resource(TaskAPI, '/api/v2/tasks/<int:task_id>')
