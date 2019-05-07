from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, optional  # optional strips white space

class positionDataForm(FlaskForm):
    nameData = StringField(label='Name of the location', validators=[DataRequired()])

    xData = DecimalField(label='First coordinate', rounding=None, validators=[DataRequired(), optional()])

    yData = DecimalField(label='Second coordinate', rounding=None, validators=[DataRequired(), optional()])

    submit = SubmitField('Add data')
