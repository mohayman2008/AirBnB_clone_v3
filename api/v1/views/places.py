#!/usr/bin/python3
'''View to handle the RESTful API actions for 'User' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    '''Handles "/cities/<city_id>/places" route'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400

        user_id = data.get('user_id')
        if user_id is None:
            return 'Missing user_id', 400
        if storage.get(User, user_id) is None:
            abort(404)

        name = data.get('name')
        if name is None:
            return 'Missing name', 400

        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_actions(place_id):
    '''Handles actions for "/places/<place_id>" route'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None or type(data) is not dict:
            print("Error: 400")
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'user_id', 'city_id', 'created_at',
                            'updated_at']:
                setattr(place, attr, val)
        place.save()
        return jsonify(place.to_dict()), 200
