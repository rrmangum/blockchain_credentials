#This bluepint will deal with all user management and credentials functionality 
from flask import Blueprint

credential_blueprint = Blueprint('credential', __name__, template_folder='templates')

from . import views