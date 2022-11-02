from . import user_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User

@user_blueprint.route('/')
def index():
    return render_template('/index.html')

@user_blueprint.route('/create/<name>')
def create_user(name):
    user = User(name=name, email=name+"@example.com")
    db.session.add(user)
    db.session.commit()

    return 'Created User!'