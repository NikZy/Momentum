from flask import render_template, Blueprint, request
import flaskr.models as models
from flaskr import db
from flaskr.auth import login_required

search_pb = Blueprint('search', __name__, url_prefix='/search')
@search_pb.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        tags = models.Tag.query.all()
        return render_template('search/search_page.html', tags=tags)
    elif request.method == 'POST':
        pass #TODO
