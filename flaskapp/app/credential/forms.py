from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class CredentialForm(FlaskForm):
    name = StringField("Credential Name", validators=[validators.DataRequired()])
    btn_cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})
