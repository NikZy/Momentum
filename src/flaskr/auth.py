userimport functools

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
        mail = request.form['mail']
        type = request.form['type']

        # for jobbsøker: TODO Linke disse opp mot et form
        kompetanse = ''
        former_jobs = ''
        cv = ''
        fødselsdato = ''

        # for startup. TODO: linke disse opp mot form
        beskrivelse = ''
        oppstartsdato = ''

        db = get_db() # hente databasen
        error = None # holder styr på om det skjer noe galt

        if not username or not password or not type:
            error = 'mangler obligatoriske felter'
        elif db.execute( # hvis brukeren finnes fra før
            'SELECT user_id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                # sett inn i user tabellen
                'INSERT INTO user (username, password, mail, type) VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), mail, type,)
            )
            db.execute(
                # sett inn i jobbsøker tabellen
                """INSERT INTO jobbsøker (former_jobs, kompetanse, cv, fødselsdato)
                VALUES (?, ?, ?, ?);""",
                (former_jobs, kompetanse, cv, fødselsdato)

            )
            db.execute(
                # startup
                'INSERT INTO startup (beskrivelse, oppstartsdato) VALUES (?, ?)',
                (beskrivelse, oppstartsdato)
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
        user = db.execute(                                          #henter bruker fra db
            'SELECT * FROM user WHERE username = ?', (username,)
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
            'SELECT * FROM user WHERE id = ?', (user_id,)
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
