#!/usr/bin/python3
"""
Amenity objects that handles all default RESTFul API actions:
"""
from models.amenity import Amenity
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ status view function """
    my_amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in my_amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_id(amenity_id=None):
    """ status view function """
    try:
        my_amenity = storage.get(Amenity, amenity_id)
        return jsonify(my_amenity.to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id=None):
    """ status view function """
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity:
        storage.delete(my_amenity)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ status view function """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id=None):
    """ status view function """
    my_amenity = storage.get(Amenity, amenity_id)
    if not my_amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_amenity, k, v)
    my_amenity.save()
    return make_response(jsonify(my_amenity.to_dict()), 200)
