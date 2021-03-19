from flask import Flask
from config import Config

# Creates the app, and sets up the static folder (containing css and images)
# and the Config object, containing the secret key used for CSRF encryption
app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object(Config)

from app import routes