from . import credential_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models import Credential
from ..models import Wallet
from .forms import CredentialForm
from werkzeug.utils import secure_filename
from ..s3_functions import *

@credential_blueprint.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        credentials = Credential.query.all()
        return render_template("credential/index.html", credentials = credentials)
    elif request.method == 'POST':
        form = CredentialForm()
        if form.validate_on_submit():
            # Save image to S3
            img = request.files['file']
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket = os.environ['S3_CREDENTIAL_BUCKET_NAME'],
                Filename=filename,
                Key = filename
            )
            full_filename = f"https://{os.environ['S3_CREDENTIAL_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            
            # Create new credential in DB
            new_credential = Credential(
                name = form.name.data,
                url = full_filename
            )
            db.session.add(new_credential)
            db.session.commit()
            flash("Credential added!")
            return redirect(url_for("credential.index"))
    

@credential_blueprint.route("/new", methods=['GET'])
def new_credential():
    form = CredentialForm(csrf_enabled=False)
    return render_template("credential/new.html", form=form)

@credential_blueprint.route("/<int:id>", methods=['DELETE'])
def delete_credential(id):
    credential = Credential.query.get(id)
    db.session.delete(credential)
    db.session.commit()
    flash("Credential deleted!")
    return jsonify({})

@credential_blueprint.route("/<int:id>", methods=['GET'])
def edit_credential(id):
    credential = Credential.query.get(id)
    form = CredentialForm(obj=credential, csrf_enabled=False)
    return render_template("credential/edit.html", form=form, credential=credential)

@credential_blueprint.route("/assign/<int:id>", methods=['GET', 'POST'])
def assign_credential(id):
    credential = Credential.query.get(id)
    if request.method == 'GET':
        wallets = Wallet.query.all()
        return render_template("credential/assign.html", credential=credential, wallets=wallets)
    elif request.method == 'POST':
        wallet_ids = request.form.getlist(credCheckbox)
        for id in wallet_ids:
            pass
    