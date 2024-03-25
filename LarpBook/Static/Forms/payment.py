from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import InputRequired, Length

class PaymentMethodForm(FlaskForm):
    payment_method = StringField('Payment Method', validators=[InputRequired(), Length(max=100)])
    card_number = StringField('Card Number', validators=[InputRequired(), Length(max=100)])
    expiry_date = StringField('Expiry Date (MM/YYYY)', validators=[InputRequired(), Length(max=7)])
    cvv = StringField('CVV', validators=[InputRequired(), Length(max=100)])
    billing_address = StringField('Billing Address', validators=[InputRequired(), Length(max=100)])
    billing_postcode = StringField('Billing Postcode', validators=[InputRequired(), Length(max=100)])
    billing_city = StringField('Billing City', validators=[InputRequired(), Length(max=100)])
    billing_country = StringField('Billing Country', validators=[InputRequired(), Length(max=100)])
