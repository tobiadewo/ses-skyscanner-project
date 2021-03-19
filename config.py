import os

class Config(object):
    """Contains a secret key for CSRF encryption. The key is stored on Heroku for security reasons."""
    SECRET_KEY = os.environ.get('SECRET_KEY')