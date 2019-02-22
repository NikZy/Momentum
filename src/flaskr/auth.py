import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import flaskr.models as models
from flaskr import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Eksempel på registrering
    '''
    if request.method == 'POST':
        type = request.form['type'] # == 'Jobbsøker'
        email = request.form['email']
        error = None # Hvis denne ikke endres så er ALL GUTSHHHI

        if (db.session.query(models.Job_applicant).filter_by(email=email).one_or_none()): # TODO Endre til Job_applicant
            error = 'bruker finnes fra før'
        elif (db.session.query(models.Startup).filter_by(email=email).one_or_none()):
            error = 'bruker finnes fra før'

        elif (type == 'Job_applicant'):
            name = request.form['name']
            password = request.form['password']

            if(not name or not email or not password):
                error = 'mangler obligatoriske felter'

            if (error is None):
                user = models.Job_applicant(name=name, email=email) # TODO endre til Job_applicant
                user = models.Startup(name=name, email=email)
                models.set_password(user, password)

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('index'))
        flash(error) # viser error i frontend

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Eksempel på login
    '''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        user = db.session.query(models.AdminUser).filter(models.AdminUser.email == email).one_or_none() # ser om noen admins har det brukernavnet
        user = db.session.query(models.Job_applicant).filter(models.Job_applicant.email == email).one_or_none() # TODO endre til Job_applicant
        # user = db.session.query(models.Startup).filter(models.Startup.email == email).one_or_none() #TODO undo this line as comment


        if (user != email): # her sto det: if (user is None):  , men skjønner ikke hvorfor så bytta det
            error = 'Feil brukernavn'
        elif (not models.check_password(user, password)): # hvis feil passord
            error = 'Feil passord'

        if error is None:                                           #hvis alt stemmer. fjern alt, og redirect til en side
            session.clear()
            session['user_id'] = user.id
            session['user_type'] = 'admin'

            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(models.AdminUser).filter(models.AdminUser.id == user_id).one_or_none()

def login_required(view):           #hvis ikke logget inn, må logge inn.
    '''
    Wrapper view for alle views som krever at du er logget inn.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()                 #ødelegger cookien slik at bruker logges ut
    return redirect(url_for('index'))
