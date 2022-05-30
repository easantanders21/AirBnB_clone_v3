#!/usr/bin/python3
""" module with the app for flask """
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


def set_port_host(HBNB_API_HOST, HBNB_API_PORT):
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = '5000'


@app.errorhandler(404)
def error_404(self):
    """ error_404 view function """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ close funtion """
    storage.close()


if __name__ == "__main__":
    set_port_host(HBNB_API_HOST, HBNB_API_PORT)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, debug=True, threaded=True)
