from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    role = SelectField('Register As', choices=[('admin', 'Admin'), ('employer', 'Employer'), ('jobseeker', 'Jobseeker')])
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    submit = SubmitField('Post Job')
