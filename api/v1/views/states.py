#!/usr/bin/python3
""" Handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """Retrieves the list of all State objects"""

    all_objects = []
    for object in list(storage.all(State).values()):
        all_objects.append(object.to_dict())
    return jsonify(all_objects)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state_by_id(state_id):
    """Retrieves a State object"""

    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state_by_id(state_id):
    """Deletes a State object"""

    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_states():
    """Creating a new state"""

    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, "Missing name")

    new_object = State(**request.get_json())
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state_by_id(state_id):
    """Updates a State object"""

    kwargs = request.get_json()

    object = storage.get(State, state_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
