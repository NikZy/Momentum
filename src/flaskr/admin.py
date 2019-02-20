"""
    Admin modellen.
    Den leser fra tabellene i databasen, mapper dem 
    til Python objekter. Så lager den views for /admin
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskr import db
from flaskr import models
def register_admin(app):
    admin = Admin(app, name='falskr', template_mode='bootstrap3')
    admin.add_view(ModelView(models.AdminUser, db.session))
    admin.add_view(ModelView(models.Jobbsøker, db.session))

# create admin user
import click
from flaskr import app
@app.cli.command()
@click.argument('username')
@click.argument('password')
def create_admin(username, password):
    u = models.AdminUser(username=username)
    models.set_password(u, password)

    db.session.add(u)
    db.session.commit()

    print("Addeed admin ", u.username)

