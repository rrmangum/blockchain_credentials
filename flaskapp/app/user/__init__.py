#This blueprint will deal with all user management and auth functionality 

from flask import Blueprint

user_blueprint = Blueprint('user', __name__, template_folder='templates')

from . import views