# from flakjimport SQLAlchemy, BaseQuery
# from sqlalchemy_searchable import SearchQueryMixin
# from sqlalchemy_utils.types import TSVectorType
# from sqlalchemy_searchable import make_searchable

from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

#make_searchable() # for search

#class Job_applicant_query(BaseQuery, SearchQueryMixin):
    #pass

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50))
    frontpage_post = db.relationship('Frontpage_post', backref='AdminUser', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Job_applicant(db.Model):
    #query_class = Job_applicant_query

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, default="")
    last_name=db.Column(db.String(120), nullable=False, default="")
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    CV=db.Column(db.String(500))
    former_jobs=db.Column(db.String(200))

    #search_vector = db.Column(TSVectorType('first_name', 'last_name', 'email'))

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Startup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False, default="")
    email=db.Column(db.String(50), nullable=False, default="")
    startup_date=db.Column(db.Date)
    description=db.Column(db.String(300))
    password_hash = db.Column(db.String(128))

    def _repr_(self):
        return '<user{}>'.format(self.email)

class Job_positions(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(400))
    made=db.Column(db.Date)
    title=db.Column(db.String(32), nullable=False)
    contact_mail=db.Column(db.String(32))

    def _repr_(self):
        return '<user{}>'.format(self.title)

class Tag(db.Model):
    tagname=db.Column(db.String(32), nullable=False, primary_key=True)

    def _repr_(self):
        return '<user{}>'.format(self.tagname)

class Frontpage_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="")
    body_text=db.Column(db.String(300))
    author = db.Column(db.Integer, db.ForeignKey(AdminUser.id), nullable=False)
    made=db.Column(db.Date, default=datetime.datetime.now())
    # legge til img

    def _repr_(self):
        return '<user{}>'.format(self.title)

db.configure_mappers() # Very important for SQLAlchemy Searchable?
