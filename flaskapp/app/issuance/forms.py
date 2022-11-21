from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class RevokeForm(FlaskForm):
    revoke = SubmitField(label="Revoke")