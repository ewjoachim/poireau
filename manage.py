#!/usr/bin/env python
import os
import sys
import re


def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the caller's working
    directory.
    """
    content = []

    with open('.env.default') as file_handler:
        content += file_handler.readlines()

    try:
        with open('.env') as file_handler:
            content += file_handler.readlines()
    except IOError:
        print("You have not updated your settings by using a '.env' file. Defaults will be used.")

    env_dict = {}
    for line in content:
        match = re.match(r'^([A-Za-z_0-9]+)=(.*)$', line)
        if not match:
            continue

        key, val = match.group(1), match.group(2)
        env_dict[key] = val

    os.environ.update(env_dict)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poireau.common.settings")

    from django.core.management import execute_from_command_line

    read_env()
    execute_from_command_line(sys.argv)
