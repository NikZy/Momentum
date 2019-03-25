from flask import render_template, Blueprint
import flaskr.models as models
from flaskr import db
from flaskr.auth import login_required

startup_job_position_bp = Blueprint('job_position_bp', __name__, url_prefix='/jobPosition')

@startup_job_position_bp.route('/<int:id>/', methods=['GET'])
#@login_required
def view_job_position(id):
    job_position = models.Job_position.query.filter_by(id=id).one_or_none()
    #finne user med id nr til jobposition
    if (not job_position):
        # finner ikke stillingsannonsen
        return '404'  # TODO fikse en nice 404 page
    print("job position:", job_position)
    return render_template('profile/jobPosition.html', job_position=job_position)
        #lokasjon ut fra templates og hva du vil dytte med fra models.py
