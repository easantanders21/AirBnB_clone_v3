#!/usr/bin/python3
"""
Review objects that handles all default RESTFul API actions:
"""
from models.place import Place
from models.review import Review
from models.user import User
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id=None):
    """ status view function """
    place_key = "Place.{}".format(place_id)
    my_objs = storage.all(Place)
    review_list = []
    try:
        my_place = my_objs[place_key]
        my_reviews = my_place.reviews
        for review in my_reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id=None):
    """ status view function """
    review_key = "Review.{}".format(review_id)
    my_objs = storage.all(Review)
    try:
        my_review = my_objs[review_key]
        return jsonify(my_review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id=None):
    """ status view function """
    review_key = "Review.{}".format(review_id)
    my_objs = storage.all(Review)
    if review_key in my_objs:
        my_review = my_objs[review_key]
        storage.delete(my_review)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_post(place_id=None):
    """ status view function """
    place_key = "Place.{}".format(place_id)
    my_places = storage.all(Place)
    user_key = "User.{}".format(request.get_json().get('user_id'))
    my_users = storage.all(User)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if place_key not in my_places:
        abort(404)
    if user_key not in my_users:
        abort(404)
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    if "text" not in request.get_json():
        abort(400, description="Missing text")
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id=None):
    """ status view function """
    review_key = "Review.{}".format(review_id)
    my_objs = storage.all(Review)
    my_obj = my_objs[review_key]
    if review_key not in my_objs:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_obj, k, v)
    my_obj.save()
    return make_response(jsonify(my_obj.to_dict()), 200)
