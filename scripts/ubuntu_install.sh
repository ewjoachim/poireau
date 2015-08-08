#! /usr/bin/env bash

# System-wide Dependecies and tools
# You can probably install all these with homebrew on OSX
echo "sudo apt-get install git python3 python3-dev g++ gettext libpq-dev"
sudo apt-get install git python3 python3-dev g++ gettext libpq-dev

# Get the Poireau source
git clone https://github.com/ewjoachim/poireau.git

# Create a virtualenv with python3
# This would be th normal way :
# python3 -m venv poireau

# But on Ubuntu 14.04 (trusty), a bug forces to do it like in 2 steps :
# https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847
python3 -m venv --without-pip ~/Envs/poireau
curl -L https://bootstrap.pypa.io/get-pip.py | ~/Envs/poireau/bin/python

cd poireau/
# Install the python requirements
~/Envs/poireau/bin/pip install -r requirements.txt

source ~/Envs/poireau/bin/activate

# Create the database
./manage.py migrate

echo "Creating a superuser. Please enter the username and password you want to use."
# create a superuser
./manage.py createsuperuser

# preparing the static files
./manage.py collectstatic --noinput

# preparing the translations
./scripts/compilemessages.sh
