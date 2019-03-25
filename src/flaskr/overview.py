import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime
from flaskr import models
from flaskr import db
import os
from flaskr import app

overview_bp = Blueprint('overview', __name__, url_prefix='/overview')

@overview_bp.route('/Startups/')
def Startups():
    return render_template('overview/Startups.html')

@overview_bp.route('/Job_applicants/')
def Job_applicants():
    return render_template('overview/Job_applicants.html')

@overview_bp.route('/Job_positions/')
def Job_positions():
    return render_template('overview/Job_positions.html')