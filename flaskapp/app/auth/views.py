from . import auth_blueprint
from flask import render_template, request, redirect, url_for

@auth_blueprint.route('/')
def index():
    return render_template('auth/register.html')