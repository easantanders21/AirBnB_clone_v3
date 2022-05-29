#!/usr/bin/python3
""" index file to shoe responses of request """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ status view function """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ status view function """
    dict_classes = {}
    for k, v in classes.items():
        dict_classes[k] = storage.count(v)
    return jsonify(dict_classes)
