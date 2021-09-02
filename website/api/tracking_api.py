from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort, make_response
import sqlalchemy
from ..models import Note, Tracking, tracking_schema, all_trackings_schema
from .. import db
from libs.external_api.shippo_api import Shippo
from libs.internal_api.tracking_api import TrackingAPI
from libs.helper_functions import get_base_url_port_conditional
import shippo

tracking_api = Blueprint('tracking_api', __name__)
shippo_obj = Shippo()


# Custom Tracking API
# Create tracking object in DB
@tracking_api.route('/tracking', methods=['POST'])
def add_tracking_object():
    try:
        if len(request.json['tracking_number']) < 1 or len(request.json['tracking_carrier']) < 1:
            abort(make_response({'status_code': 400, 'message': 'You much enter a tracking number and tracking carrier'}, 400))
        else:
            tracking_number = request.json['tracking_number']
            tracking_carrier = request.json['tracking_carrier']
    except KeyError:
        abort(make_response({'status_code': 400, 'message': 'An expected value was not specified'}, 400))
    except TypeError:
        abort(make_response({'status_code': 400, 'message': 'Invalid type was specified'}, 400))

    # WHY IS EVERYTHING A SHIPPO OBJECT THAT IS A PAIN TO CONVERT INTO DICT OR JSON. JEEZ MAN!!!
    # Is there something im missing with everything being a shippo object? It is very difficult to work with and seems like bad design
    # They should at least offer something to convert it easily into dict objects
    try:
        shippo_response = shippo_obj.register_tracking_webhook(tracking_number, tracking_carrier)
    except shippo.error.InvalidRequestError as e:
        abort(make_response({'status_code': 400, 'message': e.http_body['detail']}, 400))
    except shippo.error.APIError as e:
        # TF THEIR http_status METHOD IS SWAPPED WITH http_body METHOD??? this is comical
        abort(make_response({'status_code': 400, 'message': e.http_status['detail']}, 400)) 

    if shippo_response['tracking_status'] is None:
        abort(make_response({'status_code': 404, 'message': 'Shippo API returned empty response. Most likely those tracking details do not exist'}, 404))
    else:
        tracking_status = dict(shippo_response['tracking_status'].items())
        tracking_status['substatus'] = dict(shippo_response['tracking_status']['substatus'].items())

    if shippo_response['address_from'] is None:
        address_from = dict()
    else:
        address_from = dict(shippo_response['address_from'].items())

    if shippo_response['address_to'] is None:
        address_to = dict()
    else:
        address_to = dict(shippo_response['address_to'].items())

    tracking_object = Tracking(tracking_number, address_to, address_from, tracking_status)

    db.session.add(tracking_object)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        abort(make_response({'status_code': 400, 'message': 'That tracking number already exists in the database'}, 400))

    return tracking_schema.jsonify(tracking_object)

# Update tracking object in DB
@tracking_api.route('/tracking', methods=['PUT'])
def update_tracking_object():

    if 'tracking_number' in request.json:
        tracking_number = request.json['tracking_number']
        tracking_object = Tracking.query.filter_by(tracking_number=tracking_number).first()

    if tracking_object is not None:
        address_to = request.json['address_to']
        address_from = request.json['address_from']
        tracking_status = request.json['tracking_status']

        tracking_object.tracking_number = tracking_number
        tracking_object.address_to = address_to
        tracking_object.address_from = address_from
        tracking_object.tracking_status = tracking_status

        db.session.commit()

        return tracking_schema.jsonify(tracking_object)

    else:
        abort(make_response({'status_code': 404, 'message': 'That tracking object was not found in the database'}, 404))

# Get tracking objects
@tracking_api.route('/tracking', methods=['GET'])
def get_tracking_object():
    """
    Ability to filter by tracking number by querying "/tracking?tracking_number=123456"
    """
    if 'tracking_number' in request.args:
        tracking_object = Tracking.query.filter_by(tracking_number=request.args['tracking_number']).first()

        if tracking_object is not None:
            return tracking_schema.jsonify(tracking_object)
        else:
            abort(make_response({'status_code': 404, 'message': 'That tracking object was not found in the database'}, 404))

    else:
        all_tracking_objects = Tracking.query.all()
        result = all_trackings_schema.dump(all_tracking_objects)
        return jsonify(result)

# Delete specific tracking object from DB
@tracking_api.route('/tracking', methods=['DELETE'])
def delete_tracking_object():

    if 'tracking_number' in request.args:
        tracking_object = Tracking.query.filter_by(tracking_number=request.args['tracking_number']).first()

        if tracking_object is not None:
            db.session.delete(tracking_object)
            db.session.commit()
            return tracking_schema.jsonify(tracking_object)
        else:
            abort(make_response({'status_code': 404, 'message': 'That tracking object was not found in the database'}, 404))
       
    else:
        abort(make_response({'status_code': 400, 'message': 'tracking number must be specified'}, 400))


@tracking_api.route('/tracking-webhook', methods=['POST'])
def shippo_webhook():

    tracking_api = TrackingAPI(get_base_url_port_conditional())

    print('THERE WAS A WEBHOOK RESPONSE! HOORAY IF IT WORKS!')

    tracking_number = request.json['data']['tracking_number']
    tracking_status = request.json['data']['tracking_status']
    address_to = request.json['data']['address_to']
    address_from = request.json['data']['address_from']

    tracking_obj = dict(tracking_number=tracking_number, 
                        tracking_status=tracking_status, 
                        address_to=address_to, 
                        address_from=address_from)

    response = tracking_api.put_tracking_objs(body=tracking_obj)

    return response.json() 
