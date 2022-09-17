#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'User' class """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_users():
    """Retrieves the list of all Users objects"""

    all_objects = []
    for object in list(storage.all(User).values()):
        all_objects.append(object.to_dict())
    return jsonify(all_objects)


@app_views.route(
    "/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user_by_id(user_id):
    """Retrieves an User object"""

    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user_by_id(user_id):
    """Deletes an User object"""

    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_users():
    """Creating a new user"""

    if not request.get_json():
        abort(400, "Not a JSON")

    if "email" not in request.get_json().keys():
        abort(400, "Missing email")

    if "password" not in request.get_json().keys():
        abort(400, "Missing password")

    new_object = User(**request.get_json())
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user_by_id(user_id):
    """Updates an User object"""

    kwargs = request.get_json()

    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at", "email"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
