from . import wallet_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Wallet

@wallet_blueprint.route("/")
def index():
    return render_template("index.html")
