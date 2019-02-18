"""
    Admin modellen.
    Den leser fra tabellene i databasen, mapper dem 
    til Python objekter. Så lager den views for /admin
"""
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from . import db

class Models():
    def __init__(self, *args, **kwargs):
        self.Base = automap_base()
    
        # engine, suppose it has two tables 'user' and 'address' set up
        self.engine = create_engine("sqlite:///instance/flaskr.sqlite")
    
        # reflect the tables
        self.Base.prepare(self.engine, reflect=True)

        self.session = Session(self.engine)

        self.bruker = self.Base.classes.bruker
        self.forsideinnlegg = self.Base.classes.forsideinnlegg
        self.tag= self.Base.classes.tag
        

def init_db_session():
    db.init_db() # init db 
    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///instance/flaskr.sqlite")

    # reflect the tables
    Base.prepare(engine, reflect=True)

    bruker = Base.classes.bruker
    forsideinnlegg = Base.classes.forsideinnlegg
    tag= Base.classes.tag

    return Session(engine), Base


@expose('/')
def  index(self):
    arg1 = 'Hello'
    return self.render('admin/main.html', arg1=arg1)

def register_admin(app):
    Base = automap_base() # automap klasse som brukes for å scanne og mappe databasen

    # engine
    engine = create_engine("sqlite:///instance/flaskr.sqlite")
    #engine = create_engine(os.environ['SQLALCHEMY_URL'])

    # reflect the tables
    Base.prepare(engine, reflect=True)


    Session = scoped_session(sessionmaker(bind=engine))     
    session = Session() # lage en lokal db session

    # mapped classes are now created with names by default
    # matching that of the table name.
    bruker = Base.classes.bruker
    forsideinnlegg = Base.classes.forsideinnlegg
    tag= Base.classes.tag

    admin = Admin(app, name='falskr', template_mode='bootstrap3')

    # Flask and Flask-SQLAlchemy initialization here
    admin.add_view(ModelView(bruker, session))
    admin.add_view(ModelView(forsideinnlegg, session))
    admin.add_view(ModelView(tag, session))

# rudimentary relationships are produced
#session.add(bruker(brukernavn="foo",passord="123",epost="test"))
#session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
#print (bruker)