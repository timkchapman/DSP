# Import necessary modules
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length

# Define the EventForm class
class EditVenueForm(FlaskForm):
    venue = StringField('Venue', validators=[DataRequired(), Length(max=100)])
    address1 = StringField('Address Line 1', validators=[DataRequired(), Length(max=100)])
    address2 = StringField('Address Line 2', validators=[Length(max=100)])
    city = StringField('City', validators=[Length(max=100)])
    county = StringField('County', validators=[DataRequired(), Length(max=100)])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(max=10)])