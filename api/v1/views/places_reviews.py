#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'Review' class """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route(
    "/places/<place_id>/reviews", strict_slashes=False, methods=["GET"])
def get_reviews(place_id):
    """Retrieves the list of all Review objects"""

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)

    all_objects = []
    for obj in object.reviews:
        all_objects.append(obj.to_dict())
    return jsonify(all_objects)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def get_review_by_id(review_id):
    """Retrieves a Review object"""

    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    return jsonify(object.to_dict())


@app_views.route(
    "/reviews/<review_id>", strict_slashes=False, methods=["DELETE"])
def delete_review_by_id(review_id):
    """Deletes a Review object"""

    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    storage.delete(object)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/reviews", strict_slashes=False, methods=["POST"])
def post_reviews(place_id):
    """Creating a new Review"""
    if not request.get_json():
        abort(400, "Not a JSON")

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)

    if "user_id" not in request.get_json().keys():
        abort(400, "Missing user_id")

    if "text" not in request.get_json().keys():
        abort(400, "Missing text")

    object_user = storage.get(User, request.get_json()["user_id"])
    if object_user is None:
        abort(404)

    new_object = Review(**request.get_json())
    new_object.place_id = place_id
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review_by_id(review_id):
    """Updates a Review object"""

    kwargs = request.get_json()

    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in kwargs.items():
        if key not in ["id", "updated_at", "created_at",
                       "user_id", "place_id"]:
            setattr(object, key, value)
    object.save()
    return jsonify(object.to_dict()), 200
