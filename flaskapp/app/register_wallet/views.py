from . import register_wallet_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import Wallet, User
from .forms import MyForm
from datetime import datetime

@register_wallet_blueprint.route('/', methods=["GET", "POST"])
def register():
    return "Register"

@register_wallet_blueprint.route('/address=<wallet_address>', methods=['GET', 'POST'])
def register_wallet(wallet_address):
    res = Wallet.query.filter_by(address=str(wallet_address)).first()
    if res:
        res.last_connected_at = datetime.utcnow()
        db.session.commit()
        return f"Successfully updated last visit time"
    else:
        u_entry = User()
        db.session.add(u_entry)
        db.session.commit()

        user_id = u_entry.id
        w_entry = Wallet(address=wallet_address, user_id=user_id)

        db.session.add(w_entry)
        db.session.commit()
        return f"Success {wallet_address} added"
    # return render_template('index.html', form=form, wallet_address=wallet_address)