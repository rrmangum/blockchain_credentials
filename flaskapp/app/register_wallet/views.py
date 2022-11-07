from . import register_wallet_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Wallet
from .forms import MyForm

@register_wallet_blueprint.route('/', methods=["GET", "POST"])
def register():
    return "Register"

@register_wallet_blueprint.route('/address=<wallet_address>', methods=['GET', 'POST'])
def register_wallet(wallet_address):
    form = MyForm()
    return render_template('index.html', form=form, wallet_address=wallet_address)