from . import register_wallet_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Wallet
from .forms import MyForm
import random

@register_wallet_blueprint.route('/', methods=["GET", "POST"])
def register():
    return "Register"

@register_wallet_blueprint.route('/address=<wallet_address>', methods=['GET', 'POST'])
def register_wallet(wallet_address):
    entry = Wallet(address=wallet_address, user_id=33)
    db.session.add(entry)
    db.session.commit()
    return f"Success {wallet_address} added"
    # return render_template('index.html', form=form, wallet_address=wallet_address)