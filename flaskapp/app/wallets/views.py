from . import wallets_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Wallet
# from forms import MyForm


@wallets_blueprint.route("/")
def index():
    return render_template("index.html")

