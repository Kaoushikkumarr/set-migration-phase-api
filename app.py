"""
This file will be used for adding all the configurations, end-points, etc... to run the application
"""
from flask import Flask
from API.views import bp
from flask_cors import CORS
from flask_restful import Api
from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()

app = Flask(__name__)
app.register_blueprint(bp)

CORS(app)
api = Api(app)
