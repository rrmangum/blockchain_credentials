#This bluepint will deal with all user management and issuances functionality 
from flask import Blueprint

issuance_blueprint = Blueprint('issuance', __name__, template_folder='templates')

from . import views