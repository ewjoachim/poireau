# Pool Of Intelligent Records Effortlessly Auto-generated for Usability (POIREAU)

This project aims at creating an internal website to ease file management and song learning between all the members of a choir. It mainly uses Python 3, Django, Bootstrap.

Who does that ?
===============

This project is currently managed by members of the [Negitachi](http://www.negitachi.fr) choir.


How is Poireau as of now ?
==========================

Poireau is in "not even alpha state" for now. It's still going under heavy development and not ready for anything serious.

How to use the project if you're not used to working with Python3/Django projects
=================================================================================

You will find details instructions [here](tutorial.md) on how to understand the project if you're not yet used to Python3/Django development.


How to use the project if you're used to working with Python3/Django projects
=============================================================================

Requirements
------------

Except Python 3 and the requirements listed in requirements.txt, the non-python requirements for this project are :

 - Lilypond (lilypond and musicxml2ly executables) (for now, it's not used)
 - GetText for translations


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

MIT license :

Copyright © 2015, Joachim Jablon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders X be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.

Except as contained in this notice, the name of the <copyright holders> shall not be used in advertising or otherwise to promote the sale, use or other dealings in this Software without prior written authorization from the <copyright holders>.
