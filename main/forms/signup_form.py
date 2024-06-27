from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=8), Length(max=64)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(min=8), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), Length(max=128)])
    name = StringField('Name', validators=[DataRequired(), Length(min=10), Length(max=50)])
