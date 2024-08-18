from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
# Allow Cross-Origin Resource Sharing to prevent CORS errors when making requests from the front end
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
