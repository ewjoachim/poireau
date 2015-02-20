How to use the project if you're not used to working with Python/Django projects
================================================================================

Note on this guide
------------------

This guide presents the tools and projects used for the Poireau projects. If you want to install quicky the project for development on Ubuntu 14.04 LTS, please see the [ubuntu_install.sh](scripts/ubuntu_install.sh) script.

This guide should be enough for you to understand everything on this script before running it, and adapt it to your needs.

Git, Github, etc
----------------

Learn how to use Git in a fun way [here](https://try.github.io/levels/1/challenges/1)

Once this is good, you can create a GitHub account, fork this repo to your GitHub account, clone it and start coding. Don't forget GitHub has a nice graphical user interface to install on your machine to manage your local git repositery, for [Windows](https://windows.github.com/) and [Mac](https://mac.github.com/). For linux, I halighy recommand [Git-cola](https://git-cola.github.io/).

Learn Programming with Python
-----------------------------

This project uses Python 3.

There is a really good introduction on programming with Python at [intropython.org](http://introtopython.org/). Even if you code already in another language, I advise running through the course, as it explains a lot of the Python philosophy and good practices.

There's also a quick python introduction in the [Django Tutorial](http://tutorial.djangogirls.org/) linked in the django section.


VirtualEnv and Pip
------------------

I'm going to list the (as far as I can tell) best tools to have in order to ease development.
I'm mainly refering command line tools.
The explainations below will mainly focus on Linux and OSX environment.
For windows, there's also a lot of material, including [this](http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/).

1) Use pip. Pip is a python package manager that will allow instantaneous installation of all needed and unneeded python dependencies. Find information on how to install pip (along with its documentation) [here](https://pip.pypa.io/en/latest/installing.html) but the simplest way on Linux and OSX is :

    curl -L https://bootstrap.pypa.io/get-pip.py | python

On the latest versions of Python (2.7.9, 3.4), if pip is not already installed, the standard python library contains a module, ```ensurepip``` that eases the installation of pip. Pip can be added as simply as

    python -m ensurepip

With pip, you can install any package by its name by doing

    pip install [name]

where ```name``` can be a package name on [PyPI](https://pypi.python.org/pypi), a github link, a path to a folder containing a setup.py etc.

Note that when installing to a local path, you can use ```pip install -e [path]``` to install in editable mode, which means the modifications made in the folder will be take into account. Otherwise, the package will be copied to the python internal folders and will not have the subsequent modifications.

Another option pip takes is ```-r``` to point to a requirements file, a text file with the names and versions of the packages we want to install. There's such a file in the repositery, so you will be able to install all the dependecies automatically.

2) A virtual environment is a folder containing a copy of python. Especially, this python has it's own installed packages, independent from the system ```python```. This allows to install and uninstall packages for a specific project with no interaction with others ```python``` projects you may have on the side, and without the need for ```sudo```.

Virtualenvs have been added as a standard feature of ```python3```.

Create a virtualenv with

    python -m venv ~/Envs/poireau

If you have both ```python2``` and ```python3``` installed on your system, you may need to use explicitely ```python3``` :

    python3 -m venv ~/Envs/poireau

This will create a virtual environment folder named poireau in the ```"Envs"``` directory in your home. Activate it by calling

    source ~/Envs/poireau/bin/activate

on Linux / OSX, see instructions [here](https://docs.python.org/3/library/venv.html) for Windows.

To deactivate the virtualenv, simply use the command

    deactivate

which will be available only when you are "in" a virtualenv. The name of the virtualenv (the name of the folder in which it was created, here "poireau") will be displayed in your prompt once activated.

On Ubuntu 14.04 LTS (Trusty Tahr), a [bug](https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847) renders ```ensurepip``` unavailable. The workaround is to create the virtualenv without pip and to install pip manually in the virtual environment :

    python3 -m venv --without-pip ~/Envs/poireau
    curl -L https://bootstrap.pypa.io/get-pip.py | ~/Envs/poireau/bin/python

Note that once you are in a python3 venv, whatever your system ```python``` is, the ```python``` command refers to python3.

After making sure the virtualenv is activated, install all the depencies for the project by doing

    pip install -r requirements.txt


IPython
-------

Python is great for, among other things, its live shell that allows trying one's code right away. IPython is a better shell that allows lots of things like memorizing the commands you used to call them again, handle the indentation right etc. Even better, it comes with a nice Web interface named "IPython Notebook" that allows you to run code from your browser.

There are several ways to intall ipython with Notebook. One simple way is :

    sudo apt-get install ipython3 ipython3-notebook

Another way is to install it via pip, system wide or just in your environment :

    [sudo] pip install "ipython[all]"

but it assumes you have the correct libraries installed for compilation.

If you have any doubts, check the [installation instructions](http://ipython.org/ipython-doc/2/install/install.html).

Finally, note that the Notebook project is about to become "independant" of IPython, and be called [Jupyter](http://jupyter.org/)


Django
------

As far as I know, the best Django tutorial up to date is the one created by [Django Girls](http://tutorial.djangogirls.org/), an organization aiming at helping more girls to learn Django. And more boys too. And everyone.

Configure your database (for now with [sqlite3](http://www.sqlite.org/), which means you don't need a server or anything) by doing

    ./manage.py migrate


Lilypond
--------

[Lylipond](http://www.lilypond.org/) is a LaTeX module for creating scores. It's a very powerful tool that can do a lot of things and, as of now, it's the best tool we've find to transform a musicxml file to PDF and sound file. As of now, lilypond notation is generated automatically so for now, there's no real need to learn the lilypond syntax, but it may prove helpful later. Though, you will need to have lilypond installed on your machine if you plan to work on the PDF or Music generation parts.


GetText
-------

[GetText](https://www.gnu.org/software/gettext/) is a standard opensource tool to manage internationalization. It's used by Django and you'll need to install it if you want to see the Poireau project in your language (and that language is not English)

Trying it all
=============

Now that you master all the tools, you can use it all to navigate to your local git repo, activate your virtual env, and ask django to open an IPython Notebook to launch some code :

    ./manage.py shell_plus --notebook

You'll find a notebook (Poireau Notebook) that shows how to use some methods in the Django models.


Having fun
==========

You've learned a bunch of modern nice shiny tools that will definitely help you for your coding and python projects. Congratz, you're a python developer now !
