#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions:
"""
from models.state import State
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ status view function """
    my_objs = storage.all(State).values()
    my_dict = []
    for obj in my_objs:
        my_dict.append(obj.to_dict())
    return jsonify(my_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id=None):
    """ status view function """
    state_key = "State.{}".format(state_id)
    my_objs = storage.all(State)
    try:
        my_state = my_objs[state_key]
        return jsonify(my_state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id=None):
    """ status view function """
    state_key = "State.{}".format(state_id)
    my_objs = storage.all(State)
    if state_key in my_objs:
        my_state = my_objs[state_key]
        storage.delete(my_state)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ status view function """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id=None):
    """ status view function """
    state_key = "State.{}".format(state_id)
    my_objs = storage.all(State)
    my_obj = my_objs[state_key]
    if state_key not in my_objs:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(my_obj, k, v)
    my_obj.save()
    return make_response(jsonify(my_obj.to_dict()), 200)
