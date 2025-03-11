# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password'), validators=[DataRequired()]
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password'), validators=[DataRequired()]