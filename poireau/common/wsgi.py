"""
WSGI config for poireau project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poireau.common.settings")

from django.core.wsgi import get_wsgi_application

_application = get_wsgi_application()


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in environ:
        if var.startswith("POIREAU_"):
            os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)
