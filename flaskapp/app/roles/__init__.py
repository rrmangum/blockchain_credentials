#This bluepint will deal with all user management and auth functionality 

from flask import Blueprint

roles_blueprint = Blueprint('roles', __name__, template_folder='templates')

from . import views