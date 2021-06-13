from default_config import DEBUG, SQLALCHEMY_DATABASE_URI


import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")