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
        type = request.form['type']

        error = None # Hvis denne ikke endres så er ALL GUCHI

        if (type == 'jobbsøker'):
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            if(not name or not email or not password):
                error = 'mangler obligatoriske felter'
            
            #TODO må sjekke om bruker finnes i startups også
            elif (db.session.query(models.Jobbsøker).filter_by(email=email).one_or_none()):
                error = 'bruker finnes fra før'

            if (error is None):
                user = models.Jobbsøker(name=name, email=email)
                models.set_password(user, password)
                
                db.session.add(user)
                db.session.commit()
                
                return redirect(url_for('index')) # TODO endre rediregt til login siden
            flash(error) # viser error i frontend
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Eksempel på login
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        user = db.session.query(models.AdminUser).filter(models.AdminUser.username == username).one_or_none() # ser om noen admins har det brukernavnet
        # TODO legge til flere

        if (user is None):
            error = 'Feil brukernavn'
        elif (not models.check_password(user, password)): # hvis feil passord
            error = 'Feil passord'

        if error is None:
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

def login_required(view):
    '''
    Wrapper view for alle views som krever at du er loget inn.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))