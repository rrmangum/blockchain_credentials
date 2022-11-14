from . import credential_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
import json
import requests
from ..extensions import db
from ..models import Credential
from ..models import Wallet
from ..models import Issuance
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
            full_s3_filename = f"https://{os.environ['S3_CREDENTIAL_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            
            # Save image to ipfs
            img = request.files['file']
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            payload={'pinataOptions': '{"cidVersion": 1}', 'pinataMetadata': '{"name": "MyFile", "keyvalues": {"company": "unums"}}'}
            files=[
                ('file',(filename, open(filename, 'rb'), 'application/octet-stream'))
            ]
            headers = {
                'Authorization': f"Bearer {os.environ['PINATA_JWT_KEY']}"
            }
            pinata_response = requests.post(url, headers=headers, data=payload, files=files)
            
            # Create new credential in DB
            new_credential = Credential(
                name = form.name.data,
                url = full_s3_filename,
                ipfs_url = f"https://gateway.pinata.cloud/ipfs/{json.loads(pinata_response.text)['IpfsHash']}"
            )
            db.session.add(new_credential)
            db.session.commit()
            
            # Flash status message and redirect to index
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
    if request.method == 'GET':
        credential = Credential.query.get(id)
        wallets = Wallet.query.all()
        return render_template("credential/assign.html", id=id, credential=credential, wallets=wallets)
    elif request.method == 'POST':
        credential = Credential.query.get(id)
        wallet_ids = request.form.getlist('walletCheckbox')
        for id in wallet_ids:
            new_issuance = Issuance(
                wallet_id = id,
                credential_id = credential.id
            )
            db.session.add(new_issuance)
            db.session.commit()
        flash("Credential issued!")
        return redirect(url_for("credential.index"))
            
    