from . import credential_blueprint
from flask import current_app, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
import json
import requests
from ..extensions import db
from ..models import Credential, Wallet
from ..models import Wallet
from ..models import Issuance
from .forms import CredentialForm
from werkzeug.utils import secure_filename
from ..s3_functions import *
from ..w3_functions import *
from web3 import Web3

@credential_blueprint.route("/", methods=['GET', 'POST'])
@login_required
def index():
    w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/99ae78e4485c4500acc0328be6273305'))
    user = current_user
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    if request.method == 'GET':
        # Get the current user and display the credentials associated with their wallet
        user = current_user
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        credentials = Credential.query.filter_by(wallet_id=wallet.id).all()
        return render_template("credential/index.html", credentials = credentials)
    elif request.method == 'POST':
        form = CredentialForm()
        if form.validate_on_submit():
            
            # Pull in image from form upload
            img = request.files['file']
            # Secure the filename, remove weird or dangerous characters
            filename = secure_filename(img.filename)
            # Save the file in local uploads dir on server
            img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            uploaded_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            # Save image to Amazon S3
            s3.upload_file(
                Bucket = os.environ['S3_CREDENTIAL_BUCKET_NAME'],
                Filename = uploaded_image_path,
                Key = filename
            )
            full_s3_url = f"https://{os.environ['S3_CREDENTIAL_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            
            # Save image to IPFS
            pinata_base_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            payload={'pinataOptions': '{"cidVersion": 1}', 'pinataMetadata': '{"name": "vitae_credentials_file", "keyvalues": {"company": "vitae"}}'}
            files=[
                ('file',(filename, open(uploaded_image_path, 'rb'), 'application/octet-stream'))
            ]
            headers = {
                'Authorization': f"Bearer {os.environ['PINATA_JWT_KEY']}"
            }
            pinata_response = requests.post(pinata_base_url, headers=headers, data=payload, files=files)
            full_ipfs_url = f"https://gateway.pinata.cloud/ipfs/{json.loads(pinata_response.text)['IpfsHash']}"
            
            
            # Save the metadata to IPFS file
            metadata = {
                "name": form.name.data,
                "attributes": {
                    "Issuer": "Vitae.io",
                    "Expiration Date": "Indefinite"
                },
                "description": form.name.data,
                "image": full_ipfs_url,
                "external_url": "https://vitae.io"
            }
            
            with open('metadata.json', 'w') as mfp:
                json.dump(metadata, mfp)
    
            metadata_files= {"file": open("metadata.json", 'rb')}
             
            metadata_payload={'pinataOptions': '{"cidVersion": 1}', 'pinataMetadata': '{"name": "vitae_metadata_credentials_file", "keyvalues": {"company": "vitae"}}'}
            metadata_pinata_response = requests.post(pinata_base_url, headers=headers, data=metadata_payload, files=metadata_files)
            full_metadata_ipfs_url = f"https://gateway.pinata.cloud/ipfs/{json.loads(metadata_pinata_response.text)['IpfsHash']}"
            
            # Remove the temp uploaded image file
            if os.path.isfile(uploaded_image_path):
                os.remove(uploaded_image_path)
                
            # Remove the temp uploaded metadata json file
            if os.path.isfile("metadata.json"):
                os.remove("metadata.json")
            
            # Create and save new credential record in DB, along with S3 and IPFS urls
            new_credential = Credential(
                name = form.name.data,
                wallet_id = wallet.id,
                url = full_s3_url,
                ipfs_url = full_ipfs_url,
                metadata_ipfs_url = full_metadata_ipfs_url
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

@credential_blueprint.route("/<int:id>/delete")
def delete_credential(id):
    credential = Credential.query.get(id)
    db.session.delete(credential)
    db.session.commit()
    flash("Credential deleted!")
    return redirect(url_for("credential.index"))

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
            selected_wallet = Wallet.query.get(id)
            txn_hash = BestowCredential(selected_wallet.address, credential.metadata_ipfs_url)
            # readable_hash = txn_hash.blockHash.hex()

            new_issuance = Issuance(
                wallet_id = id,
                credential_id = credential.id,
                transaction_hash = txn_hash.transactionHash.hex()
            )

            db.session.add(new_issuance)
            db.session.commit()
        
        flash(f"Credential issued! {txn_hash.transactionHash.hex()}")
        return redirect(url_for("credential.index"))
        # return render_template("credential/test.html", id=id, credential=credential, txn_hash=txn_hash)

@credential_blueprint.route("/design", methods=['GET'])
def design_credential():
    return render_template("credential/design.html")