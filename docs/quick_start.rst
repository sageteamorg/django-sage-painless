Quick Start
===========

Getting Started
---------------

Before creating django project you must first create virtualenv.

.. code:: shell

    $ python3.9 -m pip install virtualenv
    $ python3.9 -m virtualenv venv

To activate virtual environment in ubuntu:

.. code:: shell

    $ source venv/bin/activate

To deactivate virtual environment use:

.. code:: shell

    $ deactivate

Start Project
-------------

First create a Django project

.. code:: shell

    $ mkdir GeneratorTutorials
    $ cd GeneratorTutorials
    $ django-admin startproject kernel .

Next we have to create a sample app that we want to generate code for it
(it is required for development. you will run tests on this app)

.. code:: shell

    $ python manage.py startapp products

Now we have to add 'products' to INSTALLED\_APPS in settings.py

.. code:: python

    INSTALLED_APPS = [
      ...
      'products',
      ...
    ]

Install Generator
-----------------

First install package

.. code:: shell

    $ pip install django-sage-painless

Then add 'sage\_painless' to INSTALLED\_APPS in settings.py

These apps should be in your INSTALLED\_APPS:

-  rest\_framework
-  drf\_yasg
-  django\_seed

.. code:: python

    INSTALLED_APPS = [
      ...
      'sage_painless',
      ...
      'rest_framework',
      'drf_yasg',
      'django_seed',
      ...
    ]
