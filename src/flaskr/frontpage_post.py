from flask import render_template, Blueprint
import flaskr.models as models
from flaskr import db

frontpage_post_bp = Blueprint('post', __name__, url_prefix='/post')
@frontpage_post_bp.route('/<int:id>/', methods=[ 'GET' ])
def view_post(id):
    print("id:",id)
    post = models.Frontpage_post.query.filter_by(id=id).one_or_none()
    print("post:", post)
    return render_template('frontpage_post/post.html', post=post)




