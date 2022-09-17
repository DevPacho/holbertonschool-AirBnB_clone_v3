#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'Amenity' classS """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_amenities():
    """Retrieves the list of all Amenity objects"""

    all_objects = []
    for object in list(storage.all(Amenity).values()):
        all_objects.append(object.to_dict())
    return jsonify(all_objects)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["GET"])
def get_amenity_by_id(amenity_id):
    """Retrieves an Amenity object"""

    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity_by_id(amenity_id):
    """Deletes an Amenity object"""

    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenities():
    """Creating a new amenity"""

    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, "Missing name")

    new_object = Amenity(**request.get_json())
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>", strict_slashes=False, methods=["PUT"])
def update_amenity_by_id(amenity_id):
    """Updates an Amenity object"""

    kwargs = request.get_json()

    object = storage.get(Amenity, amenity_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
