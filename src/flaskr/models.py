
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime



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
    def generate_data():
        admin = AdminUser(username="SuperAdmin", email="admin@admin.no")
        set_password(AdminUser, "admin")
        db.session.add(admin)

        try:
            db.session.commit()
        except:
            db.session.rollback()

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Job_applicant(db.Model):
    __tablename__ = 'Job_applicant'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, default="")
    last_name=db.Column(db.String(120), nullable=False, default="")
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    CV=db.Column(db.String(500))
    former_jobs=db.Column(db.String(200))

    def generate_data():
        job_applicant1=Job_applicant(first_name="Hanniballer",last_name="aldri", email="guns@gemale.com",CV="alt", former_jobs="morendin")
        set_password(job_applicant1,mittpassord)
        db.session.add(job_applicant1)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Startup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False, default="")
    email=db.Column(db.String(50), nullable=False, default="")
    startup_date=db.Column(db.Date)
    description=db.Column(db.String(300))
    password_hash = db.Column(db.String(128))

    def generate_data():
        startup1=Startup(name="smort",email="elon@tusk.nei", startup_date="2019-03-15",description="bra ide")
        set_password(startup1, passord1)
        db.session.add(job_applicant1)
        try:
            db.session.commit()
        except:
            db.session.rollback()


    def _repr_(self):
        return '<user{}>'.format(self.email)

class Job_positions(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(400))
    made=db.Column(db.Date)
    title=db.Column(db.String(32), nullable=False)
    contact_mail=db.Column(db.String(32))

    def generate_data():
        job_position1=Job_positions(description="kjip",made="2019-03-15",title=capn,contact_mail=viktig@transe)
        db.session.add(job_position1)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def _repr_(self):
        return '<user{}>'.format(self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname= db.Column(db.String(32))

    def generate_data():
        tag1 = Tag(tagname="IT")
        tag2 = Tag(tagname="Landbruk")
        tag3 = Tag(tagname="Økonomi og markedsføring")
        tag4 = Tag(tagname="Bygg og anlegg")
        tag5 = Tag(tagname="Off-shore")
        tag6 = Tag(tagname="Miljø")
        tag7 = Tag(tagname="Helse og sosial")
        tag8 = Tag(tagname="Design og arkitektur")
        tag9 = Tag(tagname="Elektro")
        tag10 = Tag(tagname="Hotell og reise")
        tag11 = Tag(tagname="Transport og Logistikk")
        tag12 = Tag(tagname="Musikk og kunst")
        tag13 = Tag(tagname="Sport og friluftsliv")
        tag14 = Tag(tagname="Non-profit")
        tag15 = Tag(tagname="Utdanning")
        tag16 = Tag(tagname="Journalistikk")
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.add(tag4)
        db.session.add(tag5)
        db.session.add(tag6)
        db.session.add(tag7)
        db.session.add(tag8)
        db.session.add(tag9)
        db.session.add(tag10)
        db.session.add(tag11)
        db.session.add(tag12)
        db.session.add(tag13)
        db.session.add(tag14)
        db.session.add(tag15)
        db.session.add(tag16)

        try:
            db.session.commit()
        except:
            db.session.rollback()
    def _repr_(self):
        return tagname

class Frontpage_post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="")
    body_text=db.Column(db.String(300))
    author = db.Column(db.Integer, db.ForeignKey(AdminUser.id), nullable=False)
    made=db.Column(db.Date, default=datetime.datetime.now())
    # legge til img
    def generate_data():
        post1 = Frontpage_post(title="første post", body_text="TEEST", author=1)
        post2 = Frontpage_post(title="heia",body_text="yass",author=1)
        post3 = Frontpage_post(title="store nyheter!",body_text="gratis kvikk lunsj", author=1)
        post4 = Frontpage_post(title="nede til høyre?", body_text="eller ikke",author=1)
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)

        try:
            db.session.commit()
        except:
            db.session.rollback()

    def _repr_(self):
        return '<user{}>'.format(self.title)

import click
from flaskr import app
@app.cli.command()
def seed_db ():
    db.drop_all()
    Tag.generate_data()
    Frontpage_post.generate_data()

    print("populated databse")
