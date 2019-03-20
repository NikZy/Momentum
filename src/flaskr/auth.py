import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime
import flaskr.models as models
from flaskr import db
import os
from flaskr import app

bp = Blueprint('auth', __name__, url_prefix='/auth')


def to_datetimefield(date):
    '''
    Tar en string på format 2018-03-10
    gjør om til python date object

    '''
    date = date.split('-')
    return datetime(int(date[0]), int(date[1]), int(date[2]))


def save_image(file):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    img_path = file.filename


@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Eksempel på registrering
    '''

    if request.method == 'POST':
        print(request.files)
        print(request.form)
        type = request.form['type']  # == 'Jobbsøker'
        email = request.form['email']
        error = None  # Hvis denne ikke endres så er ALL GUTSHHHI
        date = request.form['date']
        img = request.files.get['file']
        
        if (img):
            save_image(img)
            file_path = img.filename

        if (date):
            date = to_datetimefield(date)  # gjør om til python datetimefield

        if (db.session.query(models.Job_applicant).filter_by(email=email).one_or_none()):
            error = 'Bruker finnes'
        elif (db.session.query(models.Startup).filter_by(email=email).one_or_none()):
            error = 'Bruker finnes'

        elif (type == 'Job_applicant' or type == 'Startup'):
            password = request.form['password']

            if(not email or not password):
                error = 'Mangler obligatoriske felter'

            if (error is None):

                if type == "Job_applicant":
                    first_name = request.form['first_name']
                    last_name = request.form['last_name']
                    CV = request.form['CV']
                    former_jobs = request.form['former_jobs']
                    user = models.Job_applicant(
                        first_name=first_name, last_name=last_name, email=email, CV=CV, former_jobs=former_jobs)
                    print("Alt gikk greit?")
                if (type == 'Startup'):
                    name = request.form['name']
                    startup_date = date  # ble hentet fra form lenger opp
                    description = request.form['description']
                    user = models.Startup(
                        name=name, email=email, startup_date=startup_date, description=description)

                    checked_tags_string=request.form.getlist('tags') #
                    checked_tags=db.session.query(models.Tag).filter(models.Tag.tagname.in_(checked_tags_string)).all()
                    for tag in checked_tags:
                        user.tags.append(tag)
                        
                        
                
                


                models.set_password(user, password)

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('auth.login'))
        
        flash(error) # viser error i frontend

    all_tags=models.Tag.query.all()
    tags=partition_list(all_tags)

    return render_template('auth/register.html', tags=tags)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Eksempel på login
    '''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        type = None

        user = db.session.query(models.AdminUser).filter(
            models.AdminUser.email == email).one_or_none()  # ser om noen admins har det brukernavnet
        if user is not None:
            type = 'AdminUser'
        else:
            user = db.session.query(models.Job_applicant).filter(
                models.Job_applicant.email == email).one_or_none()
            if user is not None:
                type = 'Job_applicant'
            else:
                user = db.session.query(models.Startup).filter(
                    models.Startup.email == email).one_or_none()
                if user is not None:
                    type = 'Startup'

        if (user is None):  # pga .one_or_none() i user over - da finnes ikke user i databasen
            error = 'Feil brukernavn'
        elif (not models.check_password(user, password)):  # hvis feil passord
            error = 'Feil passord'

        if error is None:  # hvis alt stemmer: fjern alt, og redirect til en side
            session.clear()
            session['user_id'] = user.id
            session['user_type'] = type
            session['user_email'] = user.email

            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    email = session.get('user_email')
    type = session.get('user_type')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(models.AdminUser).filter(
            models.AdminUser.id == user_id).one_or_none()
        if g.user is None:
            g.user = db.session.query(models.Job_applicant).filter(
                models.Job_applicant.email == email).one_or_none()
        if g.user is None:
            g.user = db.session.query(models.Startup).filter(
                models.Startup.email == email).one_or_none()


def user_is_admin():
    '''
    use auth in admin panel. admin.py
    '''
    return session.get('user_type')


def login_required(view):  # hvis ikke logget inn, må logge inn.
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
    session.clear()  # ødelegger cookien slik at bruker logges ut
    return redirect(url_for('index'))


def partition_list(tag_list):
    taggers = []

    for i in range(len(tag_list)//4):
        tagcol = tag_list[i*4:((i+1)*4)]
        taggers.append(tagcol)
    return taggers
