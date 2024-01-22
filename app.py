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
    latitude = db.Column(db.Float, nullable=False)
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
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        #Check if password and confirm_password match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email address is already registered. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
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

def create_sample_data():
    # Check if sample data already exists
    if not User.query.filter_by(username='user1').first():
        # Create sample data
        user1 = User(username='user1', password='password1', email='user1@example.com')
        user2 = User(username='user2', password='password2', email='user2@example.com')

        # Add sample users to the database
        db.session.add(user1)
        db.session.add(user2)

    if not Event.query.filter_by(event_name='event1').first():
        # Create sample data
        event1 = Event(organizer_id=1, event_name='Event 1', description='Description 1', latitude=12.345, longitude=67.890)
        event2 = Event(organizer_id=2, event_name='Event 2', description='Description 2', latitude=23.456, longitude=78.901)

        # Add sample events to the database
        db.session.add(event1)
        db.session.add(event2)

    # Commit changes to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='user1').first() or not Event.query.filter_by(event_name='event1').first():
            create_sample_data()
    app.run(debug=True)