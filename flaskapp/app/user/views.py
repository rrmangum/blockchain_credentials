from . import user_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
from .forms import MyForm

@user_blueprint.route("/")
def users():
    return render_template("users.html")


@user_blueprint.route("/new", methods=['GET', 'POST'])
def new():
    username = None
    email = None
    form = MyForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
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
        form = form
    )
