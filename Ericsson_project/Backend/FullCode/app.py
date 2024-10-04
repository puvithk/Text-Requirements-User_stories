from flask import Flask, render_template, request, redirect, url_for, session, ify
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
import os
import stripe
import requests
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')
app.config['TWILIO_ACCOUNT_SID'] = os.getenv('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN')

db = SQLAlchemy(app)

stripe.api_key = app.config['STRIPE_SECRET_KEY']
twilio_client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    travel_preferences = db.Column(db., nullable=True)
    account_status = db.Column(db.String(20), default='Active')
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('operator.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    seat_availability = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db., nullable=True)
    price = db.Column(db.Float, nullable=False)
    customer_rating = db.Column(db.Float, nullable=True)
    bookings = db.relationship('Booking', backref='bus', lazy=True)

    def __repr__(self):
        return f'<Bus {self.id}>'

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    travel_time = db.Column(db.Integer, nullable=False)
    buses = db.relationship('Bus', backref='route', lazy=True)

    def __repr__(self):
        return f'<Route {self.source} to {self.destination}>'

class Operator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_information = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=True)
    buses = db.relationship('Bus', backref='operator', lazy=True)

    def __repr__(self):
        return f'<Operator {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    seat_numbers = db.Column(db., nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    booking_status = db.Column(db.String(20), default='Pending')
    transaction_id = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Booking {self.id}>'

@app.route('/')
def home():
    return render_template('index.')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        address = request.form['address']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.', error='Email already exists.')

        hashed_password = hashpw(password.encode(), gensalt()).decode()
        new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and hashpw(password.encode(), user.password.encode()).decode() == user.password:
            session['user_id'] = user.id
            return redirect(url_for('home'))

        return render_template('login.', error='Invalid email or password.')

    return render_template('login.')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/search', methods=['GET'])
def search():
    source = request.args.get('source')
    destination = request.args.get('destination')
    date = request.args.get('date')
    time = request.args.get('time')

    buses = Bus.query.join(Route).filter(Route.source == source, Route.destination == destination).filter(Bus.departure_time.strftime('%Y-%m-%d') == date).filter(Bus.departure_time.strftime('%H:%M') == time).all()

    return render_template('search_results.', buses=buses)

@app.route('/bus/<int:bus_id>')
def bus_details(bus_id):
    bus = Bus.query.get_or_404(bus_id)
    return render_template('bus_details.', bus=bus)

@app.route('/book/<int:bus_id>', methods=['POST'])
def book(bus_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    bus = Bus.query.get_or_404(bus_id)
    seat_numbers = request.form.getlist('seat_number')
    ticket_price = bus.price  len(seat_numbers)

    new_booking = Booking(user_id=user_id, bus_id=bus_id, seat_numbers=seat_numbers, ticket_price=ticket_price)
    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for('booking_confirmation', booking_id=new_booking.id))

@app.route('/booking_confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('booking_confirmation.', booking=booking)

@app.route('/payment/<int:booking_id>', methods=['POST'])
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    token = request.form['stripeToken']

    try:
        charge = stripe.Charge.create(
            amount=int(booking.ticket_price  100),
            currency='usd',
            description='Bus Ticket Booking',
            source=token
        )

        booking.transaction_id = charge.id
        booking.booking_status = 'Confirmed'
        db.session.commit()

        return ify({'success': True, 'transaction_id': charge.id})

    except stripe.error.CardError as e:
        return ify({'success': False, 'error': e.user_message})

    except Exception as e:
        return ify({'success': False, 'error': str(e)})

@app.route('/booking_history')
def booking_history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    bookings = Booking.query.filter_by(user_id=user_id).all()
    return render_template('booking_history.', bookings=bookings)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    return render_template('profile.', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.phone_number = request.form['phone_number']
    user.address = request.form['address']
    user.travel_preferences = request.form.get('travel_preferences')
    db.session.commit()

    return redirect(url_for('profile'))

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id == user_id:
        booking.booking_status = 'Cancelled'
        db.session.commit()

        # Send cancellation notification
        user = User.query.get(user_id)
        message = f"Your booking for bus {booking.bus.id} has been cancelled."
        twilio_client.messages.create(
            to=user.phone_number,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            body=message
        )

    return redirect(url_for('booking_history'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


##