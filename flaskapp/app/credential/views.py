from . import credential_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Credential
from .forms import CredentialForm
from werkzeug.utils import secure_filename
from ..s3_functions import *

@credential_blueprint.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        credentials = Credential.query.all()
        return render_template("credential/index.html", credentials = credentials)
    elif request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename=filename,
                Key = filename
            )
            msg = "Upload Done ! "
        return render_template("credential/index.html")    
    

@credential_blueprint.route("/new", methods=['GET'])
def new_credential():
    form = CredentialForm(csrf_enabled=False)
    return render_template("credential/new.html", form=form)

