How to use the project if you're not used to working with Python/Django projects
================================================================================

Git, Github, etc
----------------

Learn how to use Git in a fun way [here](https://try.github.io/levels/1/challenges/1)

Once this is good, you can create a GitHub account, fork this repo to your GitHub account, clone it and start coding. Don't forget GitHub has a nice graphical user interface to install on your machine to manage your local git repositery, for [Windows](https://windows.github.com/) and [Mac](https://mac.github.com/). For linux, I halighy recommand [Git-cola](https://git-cola.github.io/).

Learn Programming with Python
-----------------------------

There is a really good introduction on programming with Python at [intropython.org](http://introtopython.org/). Even if you code already in another language, I advise running through the course, as it explains a lot of the Python philosophy and good practices.

There's also a quick python introduction in the [Django Tutorial](http://tutorial.djangogirls.org/) linked in the django section.


VirtualEnv and Pip
------------------

I'm going to list the (as far as I can tell) best tools to have in order to ease development.
I'm mainly refering command line tools.
The explainations below will mainly focus on what I know as a developer, which is Linux and OSX environment.
For windows, other people have done it better than me [here](http://www.tylerbutler.com/2012/05/how-to-install-python-pip-and-virtualenv-on-windows-with-powershell/).

1) Use pip. Pip is a python package manager that will allow instantaneous installation of all needed and unneeded python dependencies. Find information on how to install pip (along with its documentation) [here](https://pip.pypa.io/en/latest/installing.html). With pip, you can install any package by its name by doing

    pip install [name]

Name can be a package name on [PyPI](https://pypi.python.org/pypi), a github link, a path to a folder containing a setup.py etc.

Note that when installing to a local path, you can use ```pip install -e [path]``` to install in editable mode, which means the modifications made in the folder will be take into account. Otherwise, the package will be copied to the python internal folders and will not have the subsequent modifications.

Another option pip takes is ```-r``` to point to a requirements file, a text file with the names and versions of the packages we want to install. There's such a file in the repositery, so you will be able to install all the dependecies automatically.

2) You should probably use a Virtualenv (and virtualenvwrapper, which is cool) unless you have a good reason not to.
Virtualenv allows creating and using an environment (with its own environment variables and Python libraries) for each procjet. Virtualenvwrapper is just a wrapper that adds cool functions so that it's easy to use.

Install virtualenv by doing :

    [sudo] pip install virtualenv virtualenvwrapper

This should be the only thing you have to install system-wide (thus sudo), all the subsequent python packages will be installed inside virtualenvs.

Create a virtualenv by doing :

    mkvirtualenv [name]

This will also enable the virtualenv. The next time, simply enable the virtualenv by doing :

    workon [name]

If you have forgotten the name of your env, list all virtualenvs by calling ```workon```without any arguments.

And now, you're in a virtualenv. Install all the depencies for the project by doing

    pip install -r requirements.txt

IPython
-------

Python is great for, among other things, its live shell that allows trying one's code right away. IPython is a better shell that allows lots of things like memorizing the commands you used to call them again, handle the indentation right etc. Even better, it comes with a nice Web interface named "IPython Notebook" that allows you to run code from your browser.

Please read the [installation instructions](http://ipython.org/ipython-doc/2/install/install.html) but and install IPython with :

    pip install "ipython[all]"


Django
------

As far as I know, the best Django tutorial up to date is the one created by [Django Girls](http://tutorial.djangogirls.org/), an organization aiming at helping more girls to learn Django. And more boys too. And everyone.

Configure your database (for now with sqlite3, which means you don't need a server or anything) by doing

    ./manage.py migrate


Trying it all
=============

Now that you master all the tools, you can use it all to navigate to your local git repo, activate your virtual env, and ask django to open an IPython Notebook to launch some code.

At this point, you may have

    ./manage.py shell_plus --notebook

You'll find a notebook (Poireau Notebook) that shows how to use some methods in the Django models.


Having fun
==========

You've learned a bunch of modern nice shiny tools that will definitely help you for your coding and python projects. Congratz, you're a python developer now !
