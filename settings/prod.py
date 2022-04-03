"""
Production-specific Settings.

To use me, set the environment variable:
DJANGO_SETTINGS_MODULE = settings.prod
"""

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'calm-falls-98051.herokuapp.com',
    'lush-canary.herokuapp.com',
]