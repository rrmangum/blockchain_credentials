from . import user_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
import random
from forms import MyForm

@user_blueprint.route('/')
def index():
    return render_template('/index.html')

# Handles form submission 
@user_blueprint.route("/submit", methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        username = request.form["username"]
        email = request.form["email"]
        id = random.randint(1, 1000000)
        entry = User(id, username, email)
        db.session.add(entry)
        db.session.commit()
        return redirect('/success')
    return render_template('index.html', form=form)

