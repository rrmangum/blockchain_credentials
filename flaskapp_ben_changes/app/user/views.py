from . import user_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
# from forms import MyForm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# Class for form 
class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Submit')

# @user_blueprint.route('/')
# def index():
#     return render_template('/index.html')

# Handles form submission
# Posts user info to the database
# @user_blueprint.route("/submit", methods=['POST'])
# def submit():
#     username = request.form['username']
#     email = request.form['email']
#     form = MyForm()
#     form.username = username
#     form.email = email
#     if form.validate_on_submit():
#         entry = User(username, email)
#         db.session.add(entry)
#         db.session.commit()
#         return render_template('success.html', form=form)
#     return render_template('index.html')

@user_blueprint.route("/", methods=['GET', 'POST'])
def submit():
    username = None
    email = None
    form = MyForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        username = ''
        email = ''

    return render_template('index.html', 
        username = username,
        email = email,
        form = form
    )
    
