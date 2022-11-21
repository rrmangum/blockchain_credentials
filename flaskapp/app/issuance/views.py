from . import issuance_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models import Credential
from ..models import Issuance
from .forms import RevokeForm

@issuance_blueprint.route("/<int:credential_id>", methods=['GET', 'POST'])
def index(credential_id):
    form = RevokeForm()

    if request.method == 'GET':
        credential = Credential.query.get(credential_id)
        issuances = credential.issuances 
        return render_template("issuance/index.html", issuances = issuances, credential = credential, form=form)

    elif request.method == 'POST':
        credential = Credential.query.get(credential_id)
        issuances = credential.issuances

        if form.validate_on_submit():     
            # Request the checked issuances 
            issuance_ids = request.form.getlist('issuanceCheckbox')

            # Delete the issuances that the administrator checked
            for issuance in issuance_ids:
                Issuance.query.filter_by(id=int(issuance)).delete()
            db.session.commit()
    return render_template("issuance/index.html", issuances = issuances, credential = credential, form=form)
