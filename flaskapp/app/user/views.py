from . import user_blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from ..extensions import db
from ..models import User, Credential, Wallet, Issuance
from .forms import MyForm, OptionalForm
from flask_login import login_required
from werkzeug.utils import secure_filename
from ..s3_functions import *



# Handles form and form submission, validation requires a valid email address and data for each form field
# Form is pushed to the sql database
@user_blueprint.route("/user/<user_id>", methods=['GET', 'POST'])
@login_required
def user(user_id):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    # issuances = Issuance.query.filter_by(wallet_id=wallet.id).all()
    credentials = db.session.query(Issuance).join(Credential, Issuance.credential_id==Credential.id).filter(Issuance.wallet_id == wallet.id).all()
    # credentials = []
    # for issuance in issuances:
    #     credential = Credential.query.filter_by(id=issuance.credential_id).first()
    #     credentials.append(credential)
    username = current_user.name
    email = current_user.email
    profile_image = current_user.profile_image
    created_at = current_user.created_at
    return render_template('user.html', username=username, email=email, profile_image=profile_image, created_at=created_at, wallet=wallet, credentials=credentials)


# Creates edit page for the user profile
# Updates username, email and profile image based on changes made by the user
@user_blueprint.route("/user/<user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id):
    form = OptionalForm()
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    credentials = Credential.query.filter_by(wallet_id=wallet.id).first()
    created_at = current_user.created_at 
    username = current_user.name
    email = current_user.email
    profile_image = current_user.profile_image

    if form.validate_on_submit():
        # Upload profile image to s3 bucket
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket = os.environ['S3_PROFILE_PIC_BUCKET_NAME'],
                Filename=filename,
                Key = filename
            )
            full_filename = f"https://{os.environ['S3_PROFILE_PIC_BUCKET_NAME']}.s3.amazonaws.com/{filename}"
            current_user.profile_image = full_filename


        # Update username, email, and profile image and upload to database
        username = form.username.data
        email = form.email.data
        current_user.name = username
        current_user.email = email

        db.session.commit()

        flash("User Profile Updated")
        return redirect(url_for('user.user', user_id=user_id))

    return render_template("edit.html", form=form, username=username, email=email, profile_image=profile_image, created_at=created_at, wallet=wallet)