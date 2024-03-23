from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField,IntegerField
from wtforms.validators import InputRequired, NumberRange, Length

class AddTicketForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0)])
    description = StringField('Description', validators=[InputRequired(), Length(max=1000)])
    available = BooleanField('Available')
    max_tickets = IntegerField('Maximum Tickets', validators=[InputRequired(), NumberRange(min=1)])