from app import db
from datetime import datetime


class Bag(db.Model):
    __tablename__ = 'luggage'
    bag_id = db.Column(db.String(6), primary_key=True)
    passenger_fname = db.Column(db.String(20), unique=False)
    passenger_lname = db.Column(db.String(20), unique=False)
    flight_number = db.Column(db.String(6), unique=False)
    created = db.Column(db.DateTime)

    def __init__(self, bag_id, passenger_fname=None,
                 passenger_lname=None, flight_number=None):
        self.bag_id = bag_id
        self.passenger_fname = passenger_fname
        self.passenger_lname = passenger_lname
        self.flight_number = flight_number
        self.created = datetime.utcnow()


class BagEvent(db.Model):
    __tablename__ = 'bag_event'

    id = db.Column(db.Integer, primary_key=True)
    bag_id = db.Column(
        db.String(6), db.ForeignKey("luggage.bag_id"),
        nullable=False)
    event_name = db.Column(
        db.Enum('ACCEPTED', 'SECURITY_SCREEN', 'LOADING', 'IN_TRANSIT',
                'UNLOADING', 'AT_CLAIM', 'MISSING', name='bag_events'))
    event_details = db.Column(db.String(120), unique=False)
    event_time = db.Column(db.DateTime)
    __table_args__ = (
        db.UniqueConstraint('bag_id', 'event_name', name='bag_event_uc'),)

    def __init__(self, bag_id, event_name, event_details):
        self.bag_id = bag_id
        self.event_name = event_name
        self.event_details = event_details
        self.event_time = datetime.utcnow()
