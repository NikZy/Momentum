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
            db.execute(
                # sett inn i jobbsøker tabellen
                """INSERT INTO jobbsøker (tidligerejobber, kompetanse, cv, fødselsdato)
                VALUES (?, ?, ?, ?);""",
                (tidligerejobber, kompetanse, cv, fødselsdato)
                
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
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']
        db = get_db()
        error = None
        bruker = db.execute(                                          #henter bruker fra db
            'SELECT * FROM bruker WHERE brukernavn = ?', (brukernavn,)
        ).fetchone()

        if brukernavn is None:                                            #hvis brukern ikke eksisterer
            error = 'feil brukernavn eller passord'
        elif not check_password_hash(bruker['passord'], passord):   #hvis passordet ikke stemmer
            error = 'feil brukernavn eller passord'

        if error is None:                                           #hvis alt stemmer. fjern alt, og redirect til en side
            session.clear()
            session['brukerid'] = bruker['brukerid']               #setter in brukerid i cookien. henter fra brukerdb
            return redirect(url_for('index'))

        flash(error)

    return "TODO" # TODO render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    brukerid = session.get('brukerid')                #henter brukernavn fra cookien. 

    if brukerid is None:
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