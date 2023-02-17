#!/usr/bin/python3
""" Test places search API"""
import os

import json
import requests

os.environ["HBNB_MYSQL_USER"] = "hbnb_dev"
os.environ["HBNB_MYSQL_PWD"] = "hbnb_dev_pwd"
os.environ["HBNB_MYSQL_HOST"] = "localhost"
os.environ["HBNB_MYSQL_DB"] = "hbnb_dev_db"
os.environ["HBNB_TYPE_STORAGE"] = "db"

from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


def main():
    states = ['459e021a-e794-447d-9dd2-e03b7963f7d2']
    # states = []
    cities = ['1721b75c-e0b2-46ae-8dd2-f86b62fb46e6']
    # cities = []
    amenities = []
    # Cable TV, Internet
    amenities = ['017ec502-e84a-4a0f-92d6-d97e27bb6bdf',
                 '12e9ccb4-03e4-4f82-ac3d-4fc7e3ebfbfe']

    url = 'http://0.0.0.0:5000/api/v1/places_search'
    # payload = {'states': states, 'cities': cities, 'amenities': amenities}
    payload = {}
    response = requests.post(url, data=json.dumps(payload),
                             headers={"Content-Type": "application/json"})
    print(response)
    # print(response.text)
    places = response.json()
    print(f"Number of places: {len(places)}\n\n")
    count = 1
    for place in places:
        print(f'Place #{count}: {place["id"]}')
        del place['description']
        for key, val in place.items():
            print(f'\t{key}: {val}')
        obj = storage.get(Place, place['id'])
        if obj:
            amenities = obj.amenities
            print('\tAmenities:')
            for am in amenities:
                print(f'\t\t{am.id}: {am.name}')
        count += 1
        print()


if __name__ == "__main__":
    main()
