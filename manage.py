#!/usr/bin/env python
import os
import sys
import re


def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the caller's working
    directory.
    """
    try:
        with open('.env') as file_handler:
            content = file_handler.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        match = re.match(r'^([A-Za-z_0-9]+)=(.*)$', line)
        if not match:
            continue

        key, val = match.group(1), match.group(2)

        os.environ.setdefault(key, val)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poireau.common.settings")

    from django.core.management import execute_from_command_line

    read_env()
    execute_from_command_line(sys.argv)
