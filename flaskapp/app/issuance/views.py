from . import issuance_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models import Credential
from ..models import Issuance
from .forms import RevokeForm

@issuance_blueprint.route("/<int:credential_id>", methods=['GET', 'POST'])
def index(credential_id):
    form = RevokeForm()
    credential = Credential.query.get(credential_id)
    issuances = credential.issuances
    active_issuances = [] 
    for issuance in issuances:
        if issuance.active == True:
            active_issuances.append(issuance)
    # credential_issuance = db.session.query(Credential).join(Issuance, Credential.id==Issuance.credential_id).filter(Issuance.credential_id == credential_id).all()
    


    if request.method == 'GET':
        return render_template("issuance/index.html", active_issuances = active_issuances, credential = credential, form=form)

    elif request.method == 'POST':
        
        if form.validate_on_submit():     
            # Request the revoked issuance 
            issuance_id = request.form.get('revokeButton')

            # Delete the issuances that the administrator checked
            issuance = Issuance.query.filter_by(id=int(issuance_id)).first()
            issuance.revoked = True
            issuance.active = False
            db.session.commit()
    return render_template("issuance/delete.html", active_issuances = active_issuances, credential = credential, form=form)
