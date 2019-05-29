from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, optional  # optional strips whitespace


class positionDataForm(FlaskForm):
    nameData = StringField(label='Name of the location', validators=[DataRequired()])
    xData = DecimalField(label='First coordinate', rounding=None, validators=[DataRequired(), optional()])
    yData = DecimalField(label='Second coordinate', rounding=None, validators=[DataRequired(), optional()])
    submit = SubmitField('Add data')


class usersDataForm(FlaskForm):
    usernameData = StringField(label='Username', validators=[DataRequired()])
    passwordData = PasswordField(label="User's password", validators=[DataRequired()])
    creditsData = IntegerField(label="Amount of credits added:", validators=[DataRequired()])
    submit = SubmitField('Add data')
