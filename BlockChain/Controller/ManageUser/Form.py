from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from BlockChain.models import User


class RegistrationForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The User Name Has Been Occupied')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The E-mail Has Been Occupied')


class LoginForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    job_title = StringField('Job title', validators=[DataRequired(), Length(max=20)])
    phone_num = StringField('Phone Number', validators=[DataRequired(), Length(max=11)])
    address = StringField('Address', validators=[Length(max=100)])
    gender = SelectField("Gender", choices=[('Male', 'Male'), ('Female', 'Female')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The Username Has Been Occupied')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The E-mail Has Been Occupied')


class changePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                         validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')