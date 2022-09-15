#!/usr/bin/python3
""" Starting the API! """

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":

    host = '0.0.0.0'
    port = "5000"

    if not HBNB_API_HOST:
        HBNB_API_HOST = "0.0.0.0"

    if not HBNB_API_PORT:
        HBNB_API_PORT = 5000

    print(type(HBNB_API_PORT))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, debug=True, threaded=True)
