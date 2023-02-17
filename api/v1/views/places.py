#!/usr/bin/python3
'''View to handle the RESTful API actions for 'User' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


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
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'user_id', 'city_id', 'created_at',
                            'updated_at']:
                setattr(place, attr, val)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    '''Handles search for places on the route "/places_search"'''
    params = request.get_json()
    if params is None or type(params) is not dict:
        return 'Not a JSON', 400

    cities = []
    states_ids = params.get('states')
    cities_ids = params.get('cities')
    amenities_ids = params.get('amenities')
    if (states_ids is None or len(states_ids) == 0) and\
       (cities_ids is None or len(cities_ids) == 0) and\
       (amenities_ids is None or len(amenities_ids) == 0):
        ###
        places = [place.to_dict() for place in storage.all(Place)]
        return jsonify(places)

    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                cities.extend(state.cities)
    if cities_ids:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city and city not in cities:
                cities.append(city)
    # if len(cities) == 0:
    #     places_list = storage.all(Place)
    # else:
    #     places_list = []
    #     for city in cities:
    #         places_list.extend(city.places)
    places_list = []
    for city in cities:
        if storage_t == 'db':
            places_list.extend(city.places)
        else:
            places_list.extend([place for place in storage.all(Place)
                                if place.city_id == city.id])

    amenities_ids = params.get('amenities')
    if not amenities_ids or len(amenities_ids) == 0:
        places = places_list
    else:
        places = []

        if storage_t == 'db':
            amenities = [storage.get(Amenity, id) for id in amenities_ids]
            for place in places_list:
                if all(amenity in place.amenities for amenity in amenities):
                    places.append(place)
        else:
            for place in places_list:
                if all(amenity_id in place.amenity_id
                       for amenity_id in amenities_ids):
                    places.append(place)
    places_dicts = [place.to_dict() for place in places]
    return jsonify(places_dicts)
