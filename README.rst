Django Sage Painless
====================

django-sage-painless is a useful package based on Django Web Framework & Django Rest Framework for high-level and rapid web development.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  `Project Detail <#project-detail>`__
-  `Git Rules <#git-rules>`__
-  `Get Started <#getting-started>`__
-  `Usage <#usage>`__
-  `Contribute <#contribute>`__

Project Detail
--------------

You can find all technologies we used in our project into these files:
\* Version: 1.0.0 \* Frameworks: - Django 3.2.4 \* Libraries: - Django
rest framework 3.12.4 - Jinja2 3.0.1 \* Language: Python 3.9.4

Git Rules
---------

Sage team Git Rules Policy is available here: - `Sage Git
Policy <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__

Getting Started
---------------

Before creating django project you must first create virtualenv.

.. code:: shell

    $ python3.9 -m pip install virtualenv
    $ python3.9 -m virtualenv venv

To activate virtualenvironment in ubuntu:

.. code:: shell

    $ source venv/bin/activate

To deactive vritualenvironment use:

.. code:: shell

    $ deactivate

Start Project
-------------

First create a Django project

.. code:: shell

    $ mkdir GeneratorTutorials
    $ cd GeneratorTutorials
    $ django-admin startproject kernel .

Next we have to create an sample app that we want to generate code for
it (it is required for development. you will run tests on this app)

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

These apps should be in your INSTALLED\_APPS: - 'rest\_framework' -
'drf\_yasg' - 'django\_seed'

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

Usage
-----

For generating a whole project you just need a diagram. diagram is a
json file that contains information about database tables.

`you can find examples of diagram file
here <sage_painless/docs/diagrams>`__

start to generate (it is required for development. you will run tests on
this app)

.. code:: shell

    $ python manage.py generate --app products --diagram <path to diagram>

Here system will ask you what you want to generate for your app.

If you generated api you have to add app urls to urls.py:

.. code:: python

    urlpatterns = [
      ...
      path('api/', include('products.api.urls')),
      ...
    ]

-  You have to migrate your new models

   .. code:: shell

       $ python manage.py makemigrations
       $ python manage.py migrate

-  You can run tests for your app

   .. code:: shell

       $ python manage.py test products

-  Django run server

   .. code:: shell

       $ python manage.py runserver

-  Rest API documentation is available at ``localhost:8000/api/doc/``
-  For support Rest API doc add this part to your urls.py \`\`\`python
   from rest\_framework.permissions import AllowAny from drf\_yasg.views
   import get\_schema\_view from drf\_yasg import openapi

schema\_view = get\_schema\_view( openapi.Info( title="Rest API Doc",
default\_version='v1', description="Auto Generated API Docs",
license=openapi.License(name="S.A.G.E License"), ), public=True,
permission\_classes=(AllowAny,), )

urlpatterns = [ ... path('api/doc/', schema\_view.with\_ui('redoc',
cache\_timeout=0), name='schema-swagger-ui'), ...

\`\`\ ``- Rest API documentation is available at``\ localhost:8000/api/doc/\`

Contribute
----------

Run project tests before starting to develop - ``products`` app is
required for running tests

.. code:: shell

    $ python manage.py startapp products

.. code:: python

    INSTALLED_APPS = [
      ...
      'products',
      ...
    ]

-  you have to generate everything for this app
-  diagram file is available here:
   `Diagram <sage_painless/tests/diagrams/product_diagram.json>`__

   .. code:: shell

       $ python manage.py generate --app products --diagram sage_painless/tests/diagrams/product_diagram.json

-  run tests

   .. code:: shell

       $ python manage.py test sage_painless


