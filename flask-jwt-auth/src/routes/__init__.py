# src/routes/__init__.py

from flask import Blueprint

# Create a blueprint for the routes
routes_bp = Blueprint('routes', __name__)

# Import the authentication routes
from .auth import *