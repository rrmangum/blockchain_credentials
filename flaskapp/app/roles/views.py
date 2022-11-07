from . import roles_blueprint
from flask import render_template, request, redirect, url_for
from ..extensions import db
from ..models import User
# from forms import MyForm


@roles_blueprint.route("/")
def roles():
    return render_template("roles.html")