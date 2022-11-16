#This blueprint will deal with all user management and auth functionality 

from flask import Blueprint

about_blueprint = Blueprint('about', __name__, template_folder='./templates')

from . import views