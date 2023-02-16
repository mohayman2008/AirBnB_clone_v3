#!/usr/bin/python3
'''Script that starts a RESTful API server with flask'''
from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''Teardown operations'''
    storage.close()


@app.errorhandler(404)
def error_handler_404(error):
    '''Returns the JSON {"error": "Not found"} if resource wasn't found'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
