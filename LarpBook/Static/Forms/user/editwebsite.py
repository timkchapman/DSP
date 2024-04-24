from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length

class EditWebsiteForm(FlaskForm):
    website = StringField('Website', validators=[Length(max=100)])