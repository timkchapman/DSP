from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests

geolocation_api_url ='https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDzQRqjCQsbPfVqHd1bySNkPOCMpTLFoL8'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Password1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    lattitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    #date = db.Column(db.DateTime, nullable=False)
    #time = db.Column(db.DateTime, nullable=False)

    organizer = db.relationship('User', backref='events')

def get_location():
    try:
        response = requests.post(geolocation_api_url)
        if response.status_code == 200:
            data = response.json()
            latitude = data['location']['lat']
            longitude = data['location']['lng']
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print("Error:", str(e))
        return None

# Routes
@app.route('/')
def home():
    # return 'welcome to the home page'
    return render_template('home.html')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Create Event (Requires login)
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        flash('Please log in to create an event.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        organizer_id = session['user_id']
        latitude, longitude = get_location()
        if latitude is not None and longitude is not None:
            event = Event(name=name, description=description, organizer_id=organizer_id,
                          location=f"(latitude, longitude)")

            db.session.add(event)
            db.session.commit()
            flash('Event created successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Failed to get your location. Please try again.', 'danger')
    return render_template('create_event.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)