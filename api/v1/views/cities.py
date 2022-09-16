#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'City' class """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models import storage


@app_views.route(
    "/states/<state_id>/cities", strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    """Retrieves the list of all City objects"""

    object = storage.get(State, state_id)
    if object is None:
        abort(404)

    all_objects = []
    for obj in object.cities:
        all_objects.append(obj.to_dict())
    return jsonify(all_objects)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city_by_id(city_id):
    """Retrieves a City object"""

    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city_by_id(city_id):
    """Deletes a City object"""

    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities", strict_slashes=False, methods=["POST"])
def post_cities(state_id):
    """Creating a new city"""

    if not request.get_json():
        abort(400, "Not a JSON")

    object = storage.get(State, state_id)
    if object is None:
        abort(404)

    if "name" not in request.get_json().keys():
        abort(400, "Missing name")

    new_object = City(**request.get_json())
    new_object.state_id = state_id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city_by_id(city_id):
    """Updates a City object"""

    kwargs = request.get_json()

    object = storage.get(City, city_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at", "state_id"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
