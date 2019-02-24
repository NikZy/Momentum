'''
    Hvis dere gjør endringer her må dere kjøre kommandoene:
    1) flask db migrate  # for å se endringer er blitt gjort
    2) flask db upgrade  # for å gjøre
'''
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Jobbsøker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.emai)

class Bedrift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.emai)

# TODO Add AdminUSer
