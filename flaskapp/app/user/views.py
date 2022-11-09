from . import user_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
from .forms import MyForm
from flask_login import login_required

# Functionality to be determined
# Could see user info in this section
@user_blueprint.route("/")
def users():
    return render_template("users.html")

# Handles form and form submission, validation requires a valid email address and data for each form field
# Form is pushed to the sql database
@login_required
@user_blueprint.route("/new", methods=['GET', 'POST'])
def new_user():
    username = None
    email = None
    profile_image = None
    form = MyForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            profile_image = form.profile_image.data
            entry = User(email=email, name=username)
            db.session.add(entry)
            db.session.commit()
            username = ''
            email = ''
            return render_template('success.html', form = form)
        except Exception:
            return Exception

    return render_template('new.html', 
        username = username,
        email = email,
        profile_image=profile_image,
        form = form
    )
