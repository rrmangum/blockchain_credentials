from . import wallet_blueprint

from flask import render_template, request, redirect, url_for
from flask_login import current_user
from ..extensions import db
from ..models import Wallet
from ..models import Credential
from ..models import Issuance


@wallet_blueprint.route("/")
def index():

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
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

    return render_template("index.html", wallet=wallet, both=both)
