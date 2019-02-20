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
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']
        epost = request.form['epost']
        type = request.form['type']

        # for jobbsøker: TODO Linke disse opp mot et form
        kompetanse = ''
        tidligerejobber = ''
        cv = ''
        fødselsdato = ''

        # for startup. TODO: linke disse opp mot form
        beskrivelse = ''
        oppstartsdato = ''
    
        db = get_db() # hente databasen
        error = None # holder styr på om det skjer noe galt

        if not brukernavn or not passord or not type:
            error = 'mangler obligatoriske felter'
        elif db.execute( # hvis brukeren finnes fra før
            'SELECT brukerid FROM bruker WHERE brukernavn = ?', (brukernavn,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(brukernavn)

        if error is None:
            db.execute(
                # sett inn i bruker tabellen
                'INSERT INTO bruker (brukernavn, passord, epost, type) VALUES (?, ?, ?, ?)',
                (brukernavn, generate_password_hash(passord), epost, type,)
            )
            db.commit()
            return redirect(url_for('auth.login'))

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
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM bruker WHERE brukernavn = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM bruker WHERE id = ?', (user_id,)
        ).fetchone()

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