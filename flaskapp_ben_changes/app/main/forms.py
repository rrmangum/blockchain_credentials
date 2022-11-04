from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ConnectForm(FlaskForm):
    submit = SubmitField("Connect to Network")
    