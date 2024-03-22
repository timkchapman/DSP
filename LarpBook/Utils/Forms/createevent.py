# Import necessary modules
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length

# Define the EventForm class
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired(), Length(max=100)])
    address1 = StringField('Address Line 1', validators=[DataRequired(), Length(max=100)])
    address2 = StringField('Address Line 2', validators=[Length(max=100)])
    city = StringField('City', validators=[Length(max=100)])
    county = StringField('County', validators=[DataRequired(), Length(max=100)])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(max=10)])