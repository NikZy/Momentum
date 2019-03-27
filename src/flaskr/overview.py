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
    return render_template('overview/Startups.html')

@overview_bp.route('/Job_applicants/', methods=('GET', 'POST'))
def Job_applicants():
    return render_template('overview/Job_applicants.html')

@overview_bp.route('/Job_positions/', methods=('GET', 'POST'))
def Job_positions():
    return render_template('overview/Job_positions.html')