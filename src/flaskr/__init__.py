import os

from flask import Flask
from flask import render_template
from flask_admin import Admin

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # register admin-panel
    admin = Admin(app, name='falskr', template_mode='bootstrap3')
    
    # register auth model
    from . import auth
    app.register_blueprint(auth.bp)

    # register db model
    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/')
    def hello():
        #return render_template('index.html')
        return render_template('blog/blog.frontpage.html')

    return app
