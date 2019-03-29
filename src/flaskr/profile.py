import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
import flaskr.models as models
from flaskr import db
from flaskr.auth import startup_login_required

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
        return render_template('profile/blog.jobPosition.html', user=user)

    flash(error) #Trengs denne? Kan være istedet for error_page

@profile_bp.route('/startup/<int:startup_id>/job_position/<int:job_position_id>/', methods=['GET'])
#@login_required
def view_job_position(startup_id, job_position_id):
    job_position = models.Job_position.query.filter_by(id=job_position_id).one_or_none()
    if(job_position):
        startup = models.Startup.query.filter_by(id=job_position.startup).one_or_none()
    if (not job_position):
        # finner ikke stillingsannonsen
        return '404'  # TODO fikse en nice 404 page
    print("job position:", job_position)
    return render_template('profile/jobPosition.html', user=startup, job_position=job_position)
        #lokasjon ut fra templates og hva du vil dytte med fra models.py

# TODO: Legge til login required startup
@profile_bp.route('/startup/<int:startup_id>/register_job_position', methods=['GET', 'POST'])
@startup_login_required
def register_job_position(startup_id):
    # get tags
    from flaskr.auth import partition_list, to_datetimefield
    all_tags = models.Tag.query.all()
    all_tags = partition_list(all_tags)
    if request.method == 'POST':
        startup = models.Startup.query.filter_by(id=startup_id).one_or_none()
        print(request.form)
        form = request.form
        # henter ut all data 
        desc = form.get('description')
        deadline = form.get('deadline')
        if deadline:
            deadline = to_datetimefield(deadline)
        title = form.get('title')
        contact_email = form.get('contact_mail')
        tags_from_form = form.getlist('tags')

        # opprette og lagre db modell
        job_position = models.Job_position(description=desc, 
                                            deadline=deadline, 
                                            title=title,
                                            profile_picture=startup.profile_picture,
                                            contact_mail=contact_email)
        # legge til tags 
        checked_tags=db.session.query(models.Tag).filter(models.Tag.tagname.in_(tags_from_form)).all()
        for tag in checked_tags:
            job_position.tags.append(tag)

        # legge til startup id
        job_position.startup = startup_id
        # legge til bilde?

        # save to db
        db.session.add(job_position)
        db.session.commit() 

        # redirect til startup
        return redirect(url_for('profile.view_startup', startup_id=startup_id))
    else:
        return render_template('profile/registerJobApplication.html', tags=all_tags)

def change_startup_info():
    return render_template('profile/startup') # TODO er siste pri på liste

#@profile_bp.route('/<int:id>/', methods=('GET', 'POST'))
def change_job_applicant_info():
    return render_template('profile/job_applicant') # TODO er siste pri på lista
