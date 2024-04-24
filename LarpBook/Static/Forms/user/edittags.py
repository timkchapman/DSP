from flask_wtf import FlaskForm
from wtforms import StringField

class EditTagsForm(FlaskForm):
    tags = StringField('Interests, (comma-seperated)')
