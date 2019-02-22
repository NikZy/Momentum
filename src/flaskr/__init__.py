import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create and configure the app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_mapping(
    SECRET_KEY='dev',
    FLASK_ADMIN_SWATCH='flatly',
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'sqlite.db'), #'sqlite:////flaskr.db',
    SQLALCHEMY_TRACK_MODIFICATIONS='False'
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from flaskr import models


from . import auth
app.register_blueprint(auth.bp)

# register db model
#from flaskr.models import db, User
#db.init_app(appla


# register admin-panel
from . import admin
admin.register_admin(app)


# a simple page that says hello
@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('blog/blog.frontpage.html')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'admin': models.AdminUser, 'Job_applicant': models.Job_applicant}
