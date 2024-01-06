#!/usr/bin/python3
'''
    general routes of flask
    routes:
        /status:    displays "status":"OK"
        /stats:     dispalys total for all classes
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    '''
        returns JSON of OK status
    '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def storage_counts():
    '''
        returns counts of all classes in storage
    '''
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
