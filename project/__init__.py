# project/__init_.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint


# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
