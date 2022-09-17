#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'Place' class """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route(
    "/cities/<city_id>/places", strict_slashes=False, methods=["GET"])
def get_places(city_id):
    """Retrieves the list of all Place objects"""

    object = storage.get(City, city_id)
    if object is None:
        abort(404)

    all_objects = []
    for obj in object.places:
        all_objects.append(obj.to_dict())
    return jsonify(all_objects)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place_by_id(place_id):
    """Retrieves a Place object"""

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/places/<place_id>", strict_slashes=False, methods=["DELETE"])
def delete_place_by_id(place_id):
    """Deletes a Place object"""

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", strict_slashes=False, methods=["POST"])
def post_places(city_id):
    """Creating a new Place"""
    if not request.get_json():
        abort(400, "Not a JSON")

    object = storage.get(City, city_id)
    if object is None:
        abort(404)

    if "user_id" not in request.get_json().keys():
        abort(400, "Missing user_id")

    if "name" not in request.get_json().keys():
        abort(400, "Missing name")

    object_user = storage.get(User, request.get_json()["user_id"])
    if object_user is None:
        abort(404)

    new_object = Place(**request.get_json())
    new_object.city_id = city_id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place_by_id(place_id):
    """Updates a Place object"""

    kwargs = request.get_json()

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at", "user_id", "city_id"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
