from . import wallet_blueprint
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask_login import login_required
from ..extensions import db
from ..models import Wallet
from ..models import Credential
from ..models import Issuance
from ..w3_functions import *
from web3 import Web3


@wallet_blueprint.route("/")
@login_required
def index():

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    now = datetime.utcnow()
    # issuances = Issuance.query.filter_by(wallet_id=wallet.id)

    # credentials = []
    # for issuance in issuances:
    #     credential = Credential.query.filter_by(id=issuance.credential_id).first()
    #     credentials.append(credential)
    both = (
        db.session.query(Issuance)
        .join(Credential, Issuance.credential_id == Credential.id)
        .filter(Issuance.wallet_id == wallet.id)
        .all()
    )

    

    return render_template("index.html", wallet=wallet, both=both, now=now)


#soft delete of issuance from the database
#Update so Revoked = true 
@wallet_blueprint.route("/delete/<int:id>", methods=['Post', 'GET'])
# @login_required
def delete(id):

    # wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    
    issuance_to_delete = Issuance.query.get(id)
    now = datetime.utcnow()
   

    if request.method == "POST":
        issuance_to_delete.deleted_at = now
        token_id = request.form['token_id']
        token_id = int(token_id)
        # user = current_user.wallets[0].address

        # return render_template("delete.html",   now=now, id=id, token_id=int(token_id), user=user  )

        # try:
            
        DeleteCredential(token_id, current_user.wallets[0].address)

        db.session.commit()
        flash("Issuance Deleted")
        return redirect('/wallets')  

        # except:
        #     return "Something went wrong deleting"

    # else:
    #     return render_template("delete.html", issuance_to_delete=issuance_to_delete,  now=now, id=id, token_id=token_id)        



