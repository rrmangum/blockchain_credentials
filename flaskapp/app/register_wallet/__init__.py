#This blueprint will deal with all wallet management and auth functionality 

from flask import Blueprint

register_wallet_blueprint = Blueprint('register-wallet', __name__, template_folder='templates')

from . import views