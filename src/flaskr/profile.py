import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
import flaskr.models as models
from flaskr import db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

#@login_required
@profile_bp.route('/job_applicant/<int:id>/', methods=('GET', 'POST'))
def view_job_applicant(id):
    error = ''
    user = models.Job_applicant.query.filter_by(id=id).one_or_none()
    if user is None:
        error = '404 - fant ikke bruker' # TODO fikse en nice 404 page
        return render_template('error_page.html')
    else:
        # i user ligger navn, etternavn, epost, fødselsdato, tidligere_jobber, cv
        models.Job_applicant.query.filter_by(id=id).all() #??
        return render_template('profile/job_applicant.html', user=user, )
    #print("post:", post)
    #return render_template('profile/post.html', post=post)
    flash(error) #Trengs denne? Kan være istedet for error_page

@profile_bp.route('/startup/<int:id>/', methods=('GET', 'POST'))
def view_startup(id):
    error = ''
    user = models.Startup.query.filter_by(id=id).one_or_none()
    if user is None:
        error = '404 - fant ikke bruker' # TODO fikse en nice 404 page
        return render_template('error_page.html')
    else:
        # i user ligger navn, beskrivelse, stillingsannonser, opprettelsesdato, epost.
        return render_template('profile/startup.html', user=user)

    flash(error) #Trengs denne? Kan være istedet for error_page

def change_startup_info():
    return render_template('profile/startup') # TODO er siste pri på liste

#@profile_bp.route('/<int:id>/', methods=('GET', 'POST'))
def change_job_applicant_info():
    return render_template('profile/job_applicant') # TODO er siste pri på lista
