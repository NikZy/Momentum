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

@profile_bp.route('/startup/<int:startup_id>/', methods=('GET', 'POST'))
def view_startup(startup_id):
    error = ''
    user = models.Startup.query.filter_by(id=startup_id).one_or_none()
    if user is None:
        error = '404 - fant ikke bruker' # TODO fikse en nice 404 page
        return render_template('error_page.html')
    else:
        # i user ligger navn, beskrivelse, stillingsannonser, opprettelsesdato, epost.
        return render_template('profile/startup.html', user=user)

    flash(error) #Trengs denne? Kan være istedet for error_page

@profile_bp.route('/startup/<int:startup_id>/job_position/<int:job_position_id>/', methods=['GET'])
#@login_required
def view_job_position(startup_id, job_position_id):
    job_position = models.Frontpage_post.query.filter_by(id=job_position_id).one_or_none()
    if (not job_position):
        # finner ikke stillingsannonsen
        return '404'  # TODO fikse en nice 404 page
    print("job position:", job_position)
    return render_template('profile/jobPosition.html', job_position=job_position)
        #lokasjon ut fra templates og hva du vil dytte med fra models.py

# TODO: Legge til login required startup
@profile_bp.route('/startup/<int:startup_id>/register_job_position', methods=['GET', 'POST'])
def register_job_position(startup_id):
    if request.method == 'POST':
        print(request.form)
        
        # henter ut all data 

        # opprette og lagre db modell

        # redirect til startup
    else:
        return render_template('profile/registerJobApplication.html')

def change_startup_info():
    return render_template('profile/startup') # TODO er siste pri på liste

#@profile_bp.route('/<int:id>/', methods=('GET', 'POST'))
def change_job_applicant_info():
    return render_template('profile/job_applicant') # TODO er siste pri på lista
