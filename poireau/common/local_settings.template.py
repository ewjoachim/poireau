"""
local_settings.template.py is an example file.
Copy it to local_settings.py and add your specific settings.

local_settings should ever be commited.
"""

# This is important, especially for SONGS_FOLDER.


# production and project specific example settings

DEBUG = False

SECRET_KEY = "<Replace this with a long random generated string !>"

CHOIR_NAME = "Name of your choir"

SONGS_FOLDER = "/path/to/your/song/files/"

ALLOWED_HOSTS = ["your.website.com"]

ADMINS = [("John Doe", "john@doe.com")]

EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
EMAIL_PORT = 25
