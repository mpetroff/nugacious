"""
WSGI config for nugacious project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nugacious.settings")

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

env_variables_to_pass = ['NUGACIOUS_SECRET_KEY', ]
def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)
