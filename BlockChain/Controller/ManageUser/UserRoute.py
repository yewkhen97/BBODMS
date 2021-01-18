from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from BlockChain import bcrypt
from BlockChain.Controller.ManageUser.Form import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   changePasswordForm)
from BlockChain.Model.ManageUserModel.ManageUserModel import (get_user, set_new_user, set_new_admin,
                                                              set_update_data, get_account_details,set_new_password)

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('BlockRoute.home'))
    form = LoginForm()
    print("form b4 submitted")
    if form.validate_on_submit():
        print("form submitted")
        user = get_user(form)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('BlockRoute.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('ManageUser/login.html', title='Login', form=form)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('BlockRoute.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        set_new_user(form)
        flash(f'You have register account successfully! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('ManageUser/register.html', title='Register', form=form)


@users.route("/cRegister", methods=['GET', 'POST'])
def cRegister():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        set_new_admin(form)
        flash(f'You have register account successfully! You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('/cRegister.html', title='Register', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('BlockRoute.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    image_file = url_for('static', filename='profile_picture/' + current_user.image_file)
    return render_template('ManageUser/account.html', title='Account', image_file=image_file)


@users.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        set_update_data(form)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.job_title.data = current_user.job_title
        form.phone_num.data = current_user.phone_num
        form.address.data = current_user.address
        form.gender.data = current_user.gender
    image_file = url_for('static', filename='profile_picture/' + current_user.image_file)
    return render_template('ManageUser/updateAccount.html', title='Account', image_file=image_file, form=form)


@users.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = changePasswordForm()
    if form.validate_on_submit():
        set_new_password(form)
        flash('Your Password has been changed!', 'success')
        return redirect(url_for('users.account'))

    return render_template('ManageUser/change_password.html', title='Change Password', form=form,
                           legend="Update Password")
