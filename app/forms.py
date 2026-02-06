from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """Form for new user registration with validation."""
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters.')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required.'),
        Length(min=1, max=80)
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required.'),
        Length(min=1, max=80)
    ])
    
    age = IntegerField('Age', validators=[
        Optional(),
        NumberRange(min=1, max=150, message='Please enter a valid age.')
    ])
    
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=500, message='Bio cannot exceed 500 characters.')
    ])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists in database."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken.')
    
    def validate_email(self, email):
        """Check if email already exists in database."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')


class UpdateForm(FlaskForm):
    """Form for updating existing user profiles."""
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters.')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required.'),
        Length(min=1, max=80)
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required.'),
        Length(min=1, max=80)
    ])
    
    age = IntegerField('Age', validators=[
    Optional(),
    NumberRange(min=1, max=150, message='Please enter a valid age.')
])
    
    bio = TextAreaField('Bio', validators=[
        Optional(),
        Length(max=500, message='Bio cannot exceed 500 characters.')
    ])
    
    submit = SubmitField('Update Profile')