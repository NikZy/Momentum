from flask import render_template, Blueprint
import flaskr.models as models
from flaskr import db
from flaskr.auth import login_required

frontpage_post_bp = Blueprint('post', __name__, url_prefix='/post')
@frontpage_post_bp.route('/<int:id>/', methods=['GET'])
#@login_required
def view_post(id):
    post = models.Frontpage_post.query.filter_by(id=id).one_or_none()
    if (not post):
        # finner ikke posten
        return '404'  # TODO fikse en nice 404 page
    print("post:", post)
    return render_template('frontpage_post/post.html', post=post)
