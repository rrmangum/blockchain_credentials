from . import user_blueprint
from flask import render_template, request, redirect, url_for
from flask_login import current_user
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
@user_blueprint.route("/new", methods=['GET', 'POST'])
@login_required
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
            current_user.name = username
            current_user.email = email
            current_user.profile_image = profile_image
            db.session.commit()
            username = ''
            email = ''
            profile_image = ''
            return render_template('success.html', form = form)
        except Exception:
             return Exception

    return render_template('new.html', 
        username = username,
        email = email,
        profile_image=profile_image,
        form = form
    )
