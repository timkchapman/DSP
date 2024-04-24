from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class EditAboutForm(FlaskForm):
    about = StringField('About', validators=[DataRequired(), Length(min=2, max=1000)])
