from flask import render_template, Blueprint, request, redirect
import flaskr.models as models
from flaskr import db
from flaskr.auth import login_required
import uuid
from flaskr import app
import datetime

import os
api_pb = Blueprint('api', __name__, url_prefix='/api')
#Upload
@api_pb.route('/upload', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':

        file = request.files['file']
        filename = file.filename #secure_filename(file.filename)

        # Gen GUUID File Name
        fileExt = filename.split('.')[1]
        autoGenFileName = uuid.uuid4()

        newFileName = str(autoGenFileName) + '.' + fileExt

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName)    )

        #Save file Info into DB
        file = models.UploadFiles(fileName=newFileName, createdon=datetime.datetime.now(datetime.timezone.utc))

        db.session.add(file)
        db.session.commit()


    return redirect(url_for('index'))