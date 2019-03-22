"""
    Admin modellen.
    Den leser fra tabellene i databasen, mapper dem 
    til Python objekter. Så lager den views for /admin
"""
from flaskr.auth import login_required, user_is_admin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flaskr import db
from flaskr import models
def register_admin(app): #når tabell legges til legg til view
    admin = Admin(app, name='falskr', template_mode='bootstrap3')
    admin.add_view(MyView(models.AdminUser, db.session))
    admin.add_view(MyView(models.Job_applicant, db.session))
    admin.add_view(MyView(models.Startup, db.session))
    admin.add_view(MyView(models.Frontpage_post, db.session))
    admin.add_view(MyView(models.Tag, db.session))
    admin.add_view(MyView(models.Job_positions, db.session))

    #path = op.join(os.path.abspath(__file__ + "/../../"), 'static')  # need to get parent path of this code
    #admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
class MyView(ModelView):
    
    def is_accessible(self):
        return True #user_is_admin() TODO: FJERNE DETTE. GJØR AT ALLE KAN BRUKE ADMIN PANELET

# create admin user
import click
from flaskr import app
@app.cli.command()
@click.argument('email')
@click.argument('password')
def create_admin(email, password):
    u = models.AdminUser(email=email)
    models.set_password(u, password)

    db.session.add(u)
    db.session.commit()

    print("Addeed admin ", u.username)

