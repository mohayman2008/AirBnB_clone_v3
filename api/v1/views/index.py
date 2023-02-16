#!/usr/bin/python3
'''The API auxillary routes'''
from flask import jsonify

from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    '''Returns the JSON {"status": "OK"} for "/status" route'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''Returns stats for the objects in the storage for "/stats" route'''
    stats = {}
    for key, cls in classes.items():
        stats[key] = storage.count(cls)
    return jsonify(stats)
