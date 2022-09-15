#!/usr/bin/python3
"""Main file!"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    """Defines the request status"""
    return jsonify({"status": "OK"})
