import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
import flaskr.models as models
from flaskr import db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
def to_datetimefield(date):
    '''
    Tar en string på format 2018-03-10
    gjør om til python date object

    '''
    date = date.split('-')
    return datetime(int(date[0]),int(date[1]), int(date[2]))

@bp.route('/<int:id>/', methods=('GET', 'POST'))
#@login_required
def view_profile(id):
    user_id = session.get('user_id')
    if (not user_id):
        # skal jo aldri skje men kunne vært greit
        return '404'  # TODO fikse en nice 404 page
    print("post:", post)
    return render_template('frontpage_post/post.html', post=post)


def change_startup_info():
    return render_template('profile/startup')

@bp.route('/<int:id>/', methods=('GET', 'POST'))
def change_job_applicant_info():
    return render_template('profile/job_applicant')
