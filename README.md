# Pool Of Intelligent Records Effortlessly Auto-generated for Usability (POIREAU)

This project aims at creating an internal website to ease file management and song learning between all the members of a choir. It mainly uses Python 3, Django, Bootstrap.

Who does that ?
===============

This project is currently managed by members of the [Negitachi](http://www.negitachi.fr) choir.


How is Poireau as of now ?
==========================

Poireau is in "not even alpha state" for now. It still has to go under heavy development before being ready for anything serious.

How to use the project if you're not used to working with Python3/Django projects
=================================================================================

You will find details instructions [here](tutorial.md) on how to understand the project if you're not yet used to Python3/Django development.


How to use the project if you're used to working with Python3/Django projects
=============================================================================

Highway to dev
--------------

If the content of the [Ubuntu Install script](scripts/ubuntu_install.sh) is OK for you, then project installation on Ubuntu 14.04 LTS (Trusty) is as simple as :

    curl -O -L https://raw.githubusercontent.com/ewjoachim/poireau/master/scripts/ubuntu_install.sh
    chmod +x ubuntu_install.sh
    ./ubuntu_install.sh
    rm ubuntu_install.sh

This script will install the system-wide dependencies, git-clone the repo, create a venv, install the python reqs in it, create the Database, add an user (you), prepare the static files for web access and the translations.

Requirements
------------

Except Python 3 and the requirements listed in requirements.txt, the non-python requirements for this project are :

 - Lilypond (lilypond and musicxml2ly executables) (for now, it's not used)
 - GetText for translations
 - Ipython and Notebook if you want to try the project notebook (just for dev, and not mandatory)


Installation
------------
Once you have installed the non-python requirements above, git-clone'd the rep, created and activated a virtualenv :

	# Install the python dependencies
    pip install -r requirements.txt

    # Create the database
    ./manage.py migrate

    # preparing the static files
    ./manage.py collectstatic

    # preparing the translations
    ./scripts/compilemessages.sh

    # create a superuser
    ./manage.py createsuperuser


Try some features
-----------------

Via the Notebook :

    ./manage.py shell_plus --notebook

and open Poireau Notebook.

Via the the views :

	./manage.py runserver

Launch the tests
----------------

    ./manage.py test

(Note : no tests have been written so far... [TODO] anyone ?)

Translations
------------

Launch the script that parses the code to find translatable strings

    ./scripts/makemessages.sh

Once translation is written, compile it with

    ./scripts/compilemessages.sh

Project Settings
----------------

To specify the specific settings of your project, create a file at ```poireau/common/local_settings.py``` based on ```poireau/common/local_settings.py```. As long as you have not done so, you'll have a warning everytime you interact with the project.
You can create an empty file at that location to get rid of the message.

    poireau/common/local_settings.py not found or produced an ImportError. Default parameters used.


How to discuss
--------------

[Mailing List](https://groups.google.com/forum/?hl=fr#!forum/poireau)


License
-------

MIT license :

Copyright © 2015, Joachim Jablon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders X be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.

Except as contained in this notice, the name of the <copyright holders> shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from the <copyright holders>.
