#! /usr/bin/env bash

# Create the .po files for translation

# TODO : find out why --all does not work.
./manage.py makemessages -l fr

echo "Edit the .po files in the project and run scripts/compilemessages.sh to compile your translations."
