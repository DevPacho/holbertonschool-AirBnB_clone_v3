#!/usr/bin/python3
""" Handles all default RESTFul API actions for 'place_amenities'"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route(
    "places/<place_id>/amenities", strict_slashes=False, methods=["GET"])
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects"""

    object = storage.get(Place, place_id)
    if object is None:
        abort(404)

    all_objects = []
    for obj in object.amenities:
        all_objects.append(obj.to_dict())
    return jsonify(all_objects)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for obj in place.amenities:
        if obj.id == amenity_id:
            amenity_place = obj
    if amenity_place is None:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def post_amenity_to_place(place_id, amenity_id):
    """Links a Amenity object to a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for obj in place.amenities:
        if obj.id == amenity_id:
            amenity_place = obj
            return jsonify(obj.to_dict()), 200
    if amenity_place is None:
        if storage_t != 'db':
            place.amenities.append(amenity)
        else:
            place.amenities[amenity]
        storage.save()
        return jsonify(amenity.to_dict()), 201
