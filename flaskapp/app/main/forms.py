from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, IntegerField, FileField

class ConnectForm(FlaskForm):
    submit = SubmitField("Connect to Network")


class DeploySmartContractForm(FlaskForm):
    http_provider_url = StringField(
        "HTTPProvider URL", validators=[validators.DataRequired()]
    )
    chain_id =  IntegerField("Chain ID", validators=[validators.DataRequired()])

    wallet_address = StringField(
        "Wallet Address", validators=[validators.DataRequired()]
    )
    private_key = StringField("Private Key", validators=[validators.DataRequired()])

    btn_cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})
