"""
    Admin modellen.
    Den leser fra tabellene i databasen, mapper dem 
    til Python objekter. Så lager den views for /admin
"""
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def init_db_session():
    Base = automap_base()

    # engine, suppose it has two tables 'user' and 'address' set up
    engine = create_engine("sqlite:///instance/flaskr.sqlite")

    # reflect the tables
    Base.prepare(engine, reflect=True)


    return Session(engine), Base

def register_admin(app):
    Base = automap_base() # automap klasse som brukes for å scanne og mappe databasen

    # engine
    engine = create_engine("sqlite:///instance/flaskr.sqlite")

    # reflect the tables
    Base.prepare(engine, reflect=True)

    db.session = Session(engine)
    # mapped classes are now created with names by default
    # matching that of the table name.
    bruker = Base.classes.bruker
    forsideinnlegg = Base.classes.forsideinnlegg

    admin = Admin(app, name='falskr', template_mode='bootstrap3')

    # Flask and Flask-SQLAlchemy initialization here
    admin.add_view(ModelView(bruker, db.session))
    admin.add_view(ModelView(forsideinnlegg, db.session))

# rudimentary relationships are produced
#session.add(bruker(brukernavn="foo",passord="123",epost="test"))
#session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
#print (bruker)