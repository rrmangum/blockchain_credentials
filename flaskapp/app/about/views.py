from . import about_blueprint
from flask import render_template


@about_blueprint.route("/")
def about():
    return render_template('about.html')