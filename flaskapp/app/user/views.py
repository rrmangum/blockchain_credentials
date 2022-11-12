from . import user_blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from ..extensions import db
from ..models import User, Credential, Wallet
from .forms import MyForm, OptionalForm
from flask_login import login_required

# Handles form and form submission, validation requires a valid email address and data for each form field
# Form is pushed to the sql database
@user_blueprint.route("/", methods=['GET', 'POST'])
@login_required
def new_user():
    user = User.query.get(current_user.id)
    if not user.name:
        request.method = "POST"
    if request.method == "POST":
        username = None
        email = None
        profile_image = None
        form = MyForm()

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            profile_image = form.profile_image.data
            current_user.name = username
            current_user.email = email
            current_user.profile_image = profile_image

            # img = request.files['file']
            # filename = secure_filename(img.filename)
            # img.save(filename)
            # s3.upload_file(
            #     Bucket = os.environ['S3_PROFILE_PIC_BUCKET_NAME'],
            #     Filename=filename,
            #     Key = filename
            # )
            # full_filename = f"https://{os.environ['S3_PROFILE_PIC_BUCKET_NAME']}.s3.amazonaws.com/{filename}"


            db.session.commit()
            username = ''
            email = ''
            profile_image = ''
            flash(f"User {username} Created")
            return render_template('success.html', form = form)
        else:
            flash("Invalid Entry")


        return render_template('new.html', 
            username = username,
            email = email,
            profile_image=profile_image,
            form = form
        )
    elif request.method == "GET":
        wallet = Wallet.query.filter_by(user_id=current_user.id).first()
        credentials = Credential.query.filter_by(wallet_id=wallet.id).first()
        username = current_user.name
        email = current_user.email
        profile_image = current_user.profile_image
        created_at = current_user.created_at
        return render_template('profile.html', username=username, email=email, profile_image=profile_image, created_at=created_at, wallet=wallet)

@user_blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = OptionalForm()
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    credentials = Credential.query.filter_by(wallet_id=wallet.id).first()
    cur_image = current_user.profile_image
    cur_username = current_user.name
    cur_email = current_user.email
    cur_profile_image = current_user.profile_image
    created_at = current_user.created_at

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        profile_image = form.profile_image.data
        current_user.name = username
        current_user.email = email
        current_user.profile_image = profile_image

        # img = request.files['file']
        # filename = secure_filename(img.filename)
        # img.save(filename)
        # s3.upload_file(
        #     Bucket = os.environ['S3_PROFILE_PIC_BUCKET_NAME'],
        #     Filename=filename,
        #     Key = filename
        # )
        # full_filename = f"https://{os.environ['S3_PROFILE_PIC_BUCKET_NAME']}.s3.amazonaws.com/{filename}"

        db.session.commit()

        flash("User Profile Updated")
        return redirect("/users")
    return render_template("edit.html", form=form, username=cur_username, email=cur_email, profile_image=cur_profile_image, created_at=created_at, wallet=wallet)