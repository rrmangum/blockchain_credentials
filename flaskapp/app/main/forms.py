from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class ConnectForm(FlaskForm):
    submit = SubmitField("Connect to Network")


class SmartContractForm(FlaskForm):
    name = StringField("Smart Contract Name", validators=[validators.DataRequired()])
    btn_cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})
