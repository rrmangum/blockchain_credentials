#This bluepint will deal with all user management and auth functionality 

from flask import Wallet

wallets_blueprint = Blueprint('wallets', __name__, template_folder='templates')

from . import views