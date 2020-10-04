from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError,TextAreaField
from wtforms.validators import data_required, email, length, EqualTo
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           data_required(), length(min=2, max=20)])
    email = StringField('Email', validators=[data_required(), email()])
    password = PasswordField('Password', validators=[data_required()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     data_required(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
       
        user = User.query.filter_by(username=username.data).first()
        if user:
            username.data = '' 
            raise ValidationError('Username is already taken, Please use different one')


    def validate_email(self, email):
        emaill = User.query.filter_by(email=email.data).first()
        if emaill:
            email.data=''
            raise ValidationError('Email already in Use')


class loginForm(FlaskForm):
    email = StringField('Email', validators=[data_required(), email()])
    password = PasswordField('Password', validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class updateAccount(FlaskForm):
    username = StringField('Username', validators=[
                           data_required(), length(min=2, max=20)])
    email = StringField('Email', validators=[data_required(), email()])
    picture = FileField('Update profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        
         if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                username.data = '' 
                raise ValidationError('Username is already taken, Please use different one ')


    def validate_email(self, email):

          if email.data != current_user.email:
            emaill = User.query.filter_by(email=email.data).first()
            if emaill:
                email.data=''
                raise ValidationError('Email already in Use')


class PostForm(FlaskForm):
    title=StringField('Title',validators=[data_required()])
    content=TextAreaField('Content',validators=[data_required()])
    submit=SubmitField('Post')
   
