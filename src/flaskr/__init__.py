import os

from flask import Flask, session, url_for
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

#db.configure_mappers() #very important!
db.create_all() # lager databasen

from . import auth
app.register_blueprint(auth.bp)

# register db model
#from flaskr.models import db, User
#db.init_app(appla


# register admin-panel
from . import admin
admin.register_admin(app)

# register blog
from . import frontpage_post
app.register_blueprint(frontpage_post.frontpage_post_bp)

# register search bp
from . import search
app.register_blueprint(search.search_pb)

# register profile bp
from . import profile
app.register_blueprint(profile.profile_bp)

# a simple page that says hello
@app.route('/')
def index():


    # TODO? flytte logikken til frontpage_post blueprint?
    frontpage_posts = models.Frontpage_post.query.limit(20).all()
    print("posts:", frontpage_posts)
    #return render_template('index.html')
    return render_template('frontpage_post/blog.frontpage.html', posts=frontpage_posts)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'admin': models.AdminUser, 'Job_applicant': models.Job_applicant}
