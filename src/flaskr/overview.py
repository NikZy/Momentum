import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr import models
from flaskr import db
import os
from flaskr import app

overview_bp = Blueprint('overview', __name__, url_prefix='')

@overview_bp.route('/Startups/', methods=('GET', 'POST'))
def Startups():
    return render_template('overview/Startups.html', results = get_startups())

@overview_bp.route('/Job_applicants/', methods=('GET', 'POST'))
def Job_applicants():
    return render_template('overview/Job_applicants.html', results = get_job_applicants())

@overview_bp.route('/Job_positions/', methods=('GET', 'POST'))
def Job_positions():
    return render_template('overview/Job_positions.html', results = get_job_positions())

 

def get_job_positions():
    results = set()

    results.update(models.Job_position.query.order_by(models.Job_position.id).all())

    return results

def get_startups():
    startups = set()

    startups.update(models.Startup.query.order_by(models.Startup.name).all())

    return startups


def get_job_applicants():

    job_applicants = set()
    
    job_applicants.update(models.Job_applicant.query.order_by(models.Job_applicant.last_name).all())

    return job_applicants
