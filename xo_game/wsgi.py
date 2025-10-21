"""
WSGI config for xo_game project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xo_game.settings')

application = get_wsgi_application()
