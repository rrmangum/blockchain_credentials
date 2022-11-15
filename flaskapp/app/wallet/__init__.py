#This bluepint will deal with all user management and auth functionality 

from flask import Blueprint

wallet_blueprint = Blueprint('wallet', __name__, template_folder='templates')

from . import views