from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, URL

# Class for form 
class MyForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    profile_image = StringField('Profile Image URL', validators=[URL()])
    submit = SubmitField()

class OptionalForm(FlaskForm):
    username = StringField('Username', validators=[])
    email = StringField('Email', validators=[Email()])
    profile_image = StringField('Profile Image URL', validators=[URL()])
    submit = SubmitField()