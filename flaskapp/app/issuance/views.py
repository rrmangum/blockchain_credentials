from . import issuance_blueprint
from flask import render_template, request, redirect, url_for, flash, jsonify
from ..extensions import db
from ..models import Credential
from ..models import Wallet
from ..models import Issuance

@issuance_blueprint.route("/<int:credential_id>", methods=['GET'])
def index(credential_id):
    if request.method == 'GET':
        credential = Credential.query.get(credential_id)
        issuances = credential.issuances
        return render_template("issuance/index.html", issuances = issuances, credential = credential)


# @issuance_blueprint.route("/individuals", methods=['GET'])
# def individuals()