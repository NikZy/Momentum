from flask import render_template, Blueprint, request
import flaskr.models as models
from flaskr import db
from flaskr.auth import login_required

from sqlalchemy import or_

search_pb = Blueprint('search', __name__, url_prefix='/search')
@search_pb.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        tags = models.Tag.query.all()
        # print("TAGS: ", tags)
        return render_template('search/search_page.html', tags=tags)
    elif request.method == 'POST':
        print("form:", request.form)

        return render_template('search/search_page.html', tags=tags)

def search_db(form, text):
    '''
    Får inn et request.form, bestående av en fritekst, og et dictianary med mulige tags.
    returnerer resultater fra databasen som oppfyller kravene for tags og fritekst.
    1 resultat for job_applicant
    1 resultat fro startups
    1 resultat for forsideinnlegg
    1 resultat for annonser

    vurderer å filtrere tekst og tags hver for seg også ta snittet av begge settene til slutt
    '''
    # filter by search text
    # text = "" # text search string from form
    # Job_application
    job_applicants = search_job_applicants(text) # søker i navn og email. returnerer et set

    # søk Startup

    # søk job_positions
    
    return job_applicants

def search_job_positions(text):
    '''
    søker på title
    returnerer et set
    '''
    results = set()

    results.update(models.Job_positions.query.filter(models.Job_positions.title.like('%{}%'.format(text))))

    return results

def search_startup(text):
    '''
    søker etter navn og email
    returnerer et set
    '''
    startups = set()
    # søk name
    startups.update(models.Startup.query.filter(models.Startup.name.like('%{}%'.format(text))).all())
    # søk email
    startups.update(models.Startup.query.filter(models.Startup.email.like('%{}%'.format(text))).all())
    return startups
    

def search_job_applicants(text):

    job_applicants = set()
    # search in first_name and last_name
    job_applicants.update(models.Job_applicant.query.filter(models.Job_applicant.first_name.like('%{}%'.format(text))).all())
    job_applicants.update(models.Job_applicant.query.filter(models.Job_applicant.last_name.like('%{}%'.format(text))).all())

    # search in email
    job_applicants.update(models.Job_applicant.query.filter(models.Job_applicant.email.like('%{}%'.format(text))))
    return job_applicants

def filter_model_by_tags(model):
    '''
    Tar in en classe (og en form eller en liste med tag navn)
    returnerer alle instanser av classen som inneholder ALLE TAGS i formen eller listen
    '''
    models_all = model.query.all()

    # get tags from db
    all_tags = models.Tag.query.all()
    # filter by tags
    for tag in all_tags:
        # if tag.tagname in form:
            # print("Tag: ",tag.tagname)

            for m in models_all:
                if tag not in m.tags:
                    models_all.pop(models_all.index(m)) # hvis den ikke inneholder tagen. Fjern den
                    print("Filtered: ", m)

    return models_all


            
    
