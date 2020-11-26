from BlockChain import db, bcrypt
from BlockChain.models import User
import os
import secrets
from PIL import Image
from flask import current_app
from flask_login import current_user


def get_user(form):
    user = User.query.filter_by(email=form.email.data).first()
    return user


def set_new_user(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, password=hashed_password, email=form.email.data, userType='normal')
    db.session.add(user)
    db.session.commit()


def set_new_admin(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, password=hashed_password, email=form.email.data, userType='admin')
    db.session.add(user)
    db.session.commit()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_picture', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def set_update_data(form):
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.job_title = form.job_title.data
    current_user.phone_num = form.phone_num.data
    current_user.address = form.address.data
    current_user.gender = form.gender.data
    db.session.commit()


def get_account_details(id):
    result=User.query.get_or_404(id)
    return result


def set_new_password(form):
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    current_user.password = hashed_password
    db.session.commit()