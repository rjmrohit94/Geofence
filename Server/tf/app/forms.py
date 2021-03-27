from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    Latitude = StringField('Latitude', validators=[DataRequired()])
    Longitude = StringField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Submit')
