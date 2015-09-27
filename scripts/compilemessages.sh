#! /usr/bin/env bash

# Create the .mo files for translation

# TODO : find out why a simple
# ./manage.py compilemessages
# does not work...

cd poireau/common
django-admin compilemessages
cd - &>/dev/null

cd poireau/songs
django-admin compilemessages
cd - &>/dev/null

cd poireau/singers
django-admin compilemessages
cd - &>/dev/null

cd poireau/dropbox_sync
django-admin compilemessages
cd - &>/dev/null
