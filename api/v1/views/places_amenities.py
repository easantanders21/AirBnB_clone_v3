#!/usr/bin/python3
"""
Review objects that handles all default RESTFul API actions:
"""
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities_of_a_place(place_id=None):
    """ status view function """
    amenities_list = []
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        for amenity in my_place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for amenity_id in my_place.amenity_ids:
            amenities_list.append(storage.get(Amenity, amenity_id).to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_to_a_place(place_id=None, amenity_id=None):
    """ status view function """
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if not my_amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if my_amenity not in my_place.amenities:
            abort(404)
        storage.delete(my_amenity)
    else:
        if amenity_id not in my_place.amenity_ids:
            abort(404)
        storage.delete(my_amenity)
    storage.save()
    dict_empty
    return make_response(jsonify(dict_empty), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_post_to_a_place(place_id=None, amenity_id=None):
    """ status view function """
    my_place = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if not my_amenity:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if my_amenity in my_place.amenities:
            return make_response(jsonify(my_amenity.to_dict()), 200)
        else:
            my_place.amenities.append(my_amenity)
    else:
        if amenity_id in my_place.amenity_ids:
            return make_response(jsonify(my_amenity.to_dict()), 200)
        else:
            my_place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(jsonify(my_amenity.to_dict()), 201)
