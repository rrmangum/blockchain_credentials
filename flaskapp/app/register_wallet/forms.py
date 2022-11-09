from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

# Class for form 
def Ethereum(form, field):
    if len(field.data) != 42 or field.data[:1] != "0x":
        raise ValidationError('Must provide a valid ethereum Address')

class MyForm(FlaskForm):
    wallet = StringField('wallet', id="walletInput", validators=[DataRequired(), Ethereum])
    submit = SubmitField()
