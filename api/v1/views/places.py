#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions:
"""
from models.city import City
from models.place import Place
from models.user import User
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id=None):
    """ status view function """
    place_list = []
    try:
        my_city = storage.get(City, city_id)
        my_places = my_city.places
        for place in my_places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id=None):
    """ status view function """
    try:
        my_place = storage.get(Place, place_id)
        return jsonify(my_place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id=None):
    """ status view function """
    my_place = storage.get(Place, place_id)
    if my_place:
        storage.delete(my_place)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_post(city_id=None):
    """ status view function """
    my_city = storage.get(City, city_id)
    if not my_city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    my_user = storage.get(User, request.get_json().get('user_id'))
    if not my_user:
        abort(404)
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    body_obj = request.get_json()
    body_obj["city_id"] = city_id
    new_place = Place(**body_obj)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id=None):
    """ status view function """
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_place, k, v)
    my_place.save()
    return make_response(jsonify(my_place.to_dict()), 200)
