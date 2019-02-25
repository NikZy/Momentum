from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class AdminUser(db.Model):
    adminid = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    frontpage_post = db.relationship('Frontpage_post', backref='AdminUser', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Job_applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, default="")
    last_name=db.Column(db.String(120), nullable=False, default="")
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    CV=db.Column(db.String(500))

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Startup(db.Model):
    startup_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False, default="")
    email=db.Column(db.String(50), nullable=False, default="")
    startup_date=db.Column(db.Date)
    description=db.Column(db.String(300))

    def _repr_(self):
        return '<user{}>'.format(self.email)

class Job_positions(db.Model):
    job_positions_id=db.Column(db.Integer, primary_key=True)
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
    author = db.Column(db.Integer, db.ForeignKey(AdminUser.adminid), nullable=False)
    made=db.Column(db.Date, default=datetime.datetime.now())
    # legge til img

    def _repr_(self):
        return '<user{}>'.format(self.title)
