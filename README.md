# Pool Of Intelligent Records Effortlessly Auto-generated for Usability (POIREAU)

This project aims at creating an internal website to ease file management and song learning between all the members of a choir.

Who does that ?
===============

This project is currently managed by members of the [Negitachi](http://www.negitachi.fr) choir.


How is Poireau as of now ?
==========================

Poireau is in "not even alpha state" for now. It's still going under heavy development and not ready for anything serious.

How to use the project if you're not used to working with Python/Django projects
================================================================================

You will find details instructions [here](tutorial.md) on how to understand the project if you're not yet used to Python/Django development.


How to use the project if you're used to working with Python/Django projects
============================================================================

Requirements
------------

Except those listed in requirements.txt, the non-python requirements for this project are :

 - Lilypond (lilypond and musicxml2ly executables)


Installation
------------

	# Install the python dependencies
    pip install -r requirements.txt

    # Create the database
    ./manage.py migrate

    # preparing the static files
    ./manage.py collectstatic

    # preparing the translations
    ./script/compilemessages.sh

    # create a superuser
    ./manage.y createsuperuser


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


How to discuss
--------------

[Mailing List](https://groups.google.com/forum/?hl=fr#!forum/poireau)


License
-------

Please don't do anything evil while we're struggling to chose our licensing form.
