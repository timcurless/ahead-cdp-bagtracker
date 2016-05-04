import binascii
import os

from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from app import db
from app.luggage.models import Bag, BagEvent

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/create', methods=['POST'])
def create():
    post_data = request.get_json(silent=True, cache=False)
    if post_data is None or not post_data:
        return jsonify(error="There is something wrong with your post data")

    bag_id = binascii.b2a_hex(os.urandom(3)).upper()
    bag = Bag(
        bag_id=bag_id,
        passenger_fname=post_data['first_name'],
        passenger_lname=post_data['last_name'],
        flight_number=post_data['flight_number'])
    db.session.add(bag)
    db.session.commit()
    created_event = BagEvent(
        bag_id, 'ACCEPTED', "Accepted at ticket counter.")
    db.session.add(created_event)
    db.session.commit()
    return jsonify(bag_id=bag_id, message='Created bag %s' % (bag_id,))


@api.route('/update', methods=['POST'])
def update():
    content = request.get_json(silent=True, cache=False)
    for key in ['bag_id', 'event_name', 'event_details']:
        if key not in content.keys():
            return jsonify(status="error",
                           message="%s is missing from payload" % (key,)), 400
    if Bag.query.get(content['bag_id']) is None:
        return jsonify(status="error",
                       message="Bag %s doesn't exist" % (content['bag_id'],)
                       ), 404

    try:
        event = BagEvent(
            content['bag_id'], content['event_name'], content['event_details'])
        db.session.add(event)
        db.session.commit()
    except IntegrityError as exception:
        print exception
        return jsonify(status="error",
                       message="Could not update bag. Invalid or existing event"
                       " for bag: %s" % (content['bag_id'],)), 400

    return jsonify(
        status="OK",
        message="Sucessfully updated bag: %s" % (content['bag_id'],)
    )


@api.route('/status/<bag>')
def status(bag):
    results = Bag.query.get(bag)
    if results is None:
        return jsonify(status="error", message="Bag %s doesn't exist" % (bag,)
                       ), 404

    event_result = BagEvent.query.filter_by(bag_id=bag).order_by(
        desc(BagEvent.event_time)).first()

    return jsonify(
        bag_id=results.bag_id,
        first_name=results.passenger_fname,
        last_name=results.passenger_lname,
        flight_number=results.flight_number,
        bag_status=event_result.event_name,
        bag_status_time=event_result.event_time.strftime(
            "%m/%d/%Y %I:%M:%S %p"),
        bag_status_details=event_result.event_details
    )
