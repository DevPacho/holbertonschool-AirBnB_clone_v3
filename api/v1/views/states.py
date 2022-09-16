#!/usr/bin/python3
""" Handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage
from api.v1 import app


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """Retrieves the list of all State objects"""

    all_states = []
    for state in list(storage.all(State).values()):
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state_by_id(state_id):
    """Retrieves a State object"""

    object = storage.get(State, state_id)
    if object is None:
        return app.not_found(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state_by_id(state_id):
    """Deletes a State object"""

    object = storage.get(State, state_id)
    if object is None:
        return app.not_found(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_states():
    """Creating a new state"""

    try:
        if "name" not in request.get_json().keys():
            return jsonify("Missing name"), 400, {'Content-Type':
                                                  'application/json'}
        new_state = State(**request.get_json())
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    except Exception:
        return jsonify("Not a JSON"), 400, {'Content-Type':
                                            'application/json'}


@app_views.route(
        "/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state_by_id(state_id):
    """Updates a State object"""

    try:
        kwargs = request.get_json()
        object = storage.get(State, state_id)
        if object is None:
            return app.not_found(404)
        for key, value in kwargs.items():
            if key not in ["id", "updated_at", "created_at"]:
                setattr(object, key, value)
        object.save()
        return jsonify(object.to_dict()), 200
    except Exception:
        return jsonify("Not a JSON"), 400, {'Content-Type':
                                            'application/json'}
