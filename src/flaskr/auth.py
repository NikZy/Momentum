import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Eksempel på registrering
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        epost = request.form['epost']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(                                            #utfører en spørring til db
            'SELECT id FROM bruker WHERE brukernavn = ?', (username,)
        ).fetchone() is not None:                                   #sjekker om brukernavn eksisterer fra før
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(                                              #hvis brukernavn ikke eksisterer, sett inn i db
                'INSERT INTO bruker (brukernavn, passord, epost) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), epost)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return "TODO" # TODO render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Eksempel på login
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(                                          #henter bruker fra db
            'SELECT * FROM bruker WHERE brukernavn = ?', (username,)
        ).fetchone()

        if user is None:                                            #hvis brukern ikke eksisterer
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):   #hvis passordet ikke stemmer
            error = 'Incorrect password.'

        if error is None:                                           #hvis alt stemmer. fjern alt, og redirect til en side
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return "TODO" # TODO render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')                #henter brukernavn fra cookien. 

    if user_id is None:
        g.user = None
    else:                                         #hvis noe fra cookie, hent bruker fra db. 
        g.user = get_db().execute(
            'SELECT * FROM bruker WHERE id = ?', (user_id,)
        ).fetchone()

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