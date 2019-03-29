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
    results = list()
    x = models.Job_position.query.all()
    results = sorted(x, key=lambda i: i.id)

    return results

def get_startups():
    results = list()
    x = models.Startup.query.all()
    results = sorted(x, key=lambda i: i.name)

    return results


def get_job_applicants():
    results = list()
    x = models.Job_applicant.query.all()
    results = sorted(x, key=lambda i: i.last_name)

    return results
