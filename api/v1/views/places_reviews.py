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
    review_list = []
    try:
        my_place = storage.get(Place, place_id)
        my_reviews = my_place.reviews
        for review in my_reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id=None):
    """ status view function """
    try:
        my_review = storage.get(Review, review_id)
        return jsonify(my_review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id=None):
    """ status view function """
    my_review = storage.get(Review, review_id)
    if my_review:
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
    my_places = storage.get(Place, place_id)
    if not my_places:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    my_users = storage.get(User, request.get_json().get('user_id'))
    if not my_users:
        abort(404)
    if "text" not in request.get_json():
        abort(400, description="Missing text")
    body_obj = request.get_json()
    body_obj["place_id"] = place_id
    new_review = Review(**body_obj)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(review_id=None):
    """ status view function """
    my_review = storage.get(Review, review_id)
    if not my_review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_review, k, v)
    my_review.save()
    return make_response(jsonify(my_review.to_dict()), 200)
