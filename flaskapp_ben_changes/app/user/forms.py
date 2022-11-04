from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

# Class for form 
class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])