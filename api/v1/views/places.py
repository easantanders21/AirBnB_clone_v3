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
    city_key = "City.{}".format(city_id)
    my_objs = storage.all(City)
    place_list = []
    try:
        my_city = my_objs[city_key]
        my_places = my_city.places
        for place in my_places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id=None):
    """ status view function """
    place_key = "Place.{}".format(place_id)
    my_objs = storage.all(Place)
    try:
        my_place = my_objs[place_key]
        return jsonify(my_place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id=None):
    """ status view function """
    place_key = "Place.{}".format(place_id)
    my_objs = storage.all(Place)
    if place_key in my_objs:
        my_place = my_objs[place_key]
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
    city_key = "City.{}".format(city_id)
    my_cities = storage.all(City)
    user_key = "User.{}".format(request.get_json().get('user_id'))
    my_users = storage.all(User)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if city_key not in my_cities:
        abort(404)
    if user_key not in my_users:
        abort(404)
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id=None):
    """ status view function """
    place_key = "Place.{}".format(place_id)
    my_objs = storage.all(Place)
    my_obj = my_objs[place_key]
    if place_key not in my_objs:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_obj, k, v)
    my_obj.save()
    return make_response(jsonify(my_obj.to_dict()), 200)
