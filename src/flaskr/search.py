from flask import render_template, Blueprint, request, url_for
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
        tags_from_db = models.Tag.query.all();
        for tag in tags_from_db:
            if tag.tagname in request.form:
                print("TRUE: ", tag.tagname)
                resultat += tag.tagname;
            print(resultat)
        return render_template('search/search_page.html', tags=tags_from_db, resultat=request.form)

def search_db(form):
    print("OK")

    '''
    Får inn et request.form, bestående av en fritekst, og et dictianary med mulige tags.
    returnerer resultater fra databasen som oppfyller kravene for tags og fritekst.
    1 resultat for job_applicant
    1 resultat for startups
    1 resultat for forsideinnlegg
    1 resultat for annonser

    '''
    pass
