Django Sage Painless
====================

django-sage-painless is a useful package based on Django Web Framework & Django Rest Framework for high-level and rapid web development.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|SageTeam|

|PyPI release| |Supported Python versions| |Supported Django
versions| |Documentation| |Build|

-  `Project Detail <#project-detail>`__
-  `Git Rules <#git-rules>`__
-  `Get Started <#getting-started>`__
-  `Usage <#usage>`__
-  `Contribute <#contribute>`__

Project Detail
--------------

\* Frameworks: - Django > 3.1 \* Language: Python > 3.6

Git Rules
---------

Sage team Git Rules Policy is available here:

-  `Sage Git
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
      'products',
    ]

Install Generator
-----------------

First install package

.. code:: shell

    $ pip install django-sage-painless

Then add 'sage\_painless' to INSTALLED\_APPS in settings.py

These apps should be in your INSTALLED\_APPS:

-  'rest\_framework'
-  'drf\_yasg'
-  'django\_seed'

.. code:: python

    INSTALLED_APPS = [
      'sage_painless',
      'rest_framework',
      'drf_yasg',
      'django_seed',
    ]

Usage
-----

For generating a whole project you just need a diagram. diagram is a
json file that contains information about database tables.

`you can find examples of diagram file
here <sage_painless/docs/diagrams>`__

start to generate (it is required for development. you will run tests on
this app)

First validate the format of your diagram

.. code:: shell

    $ python manage.py validate_diagram --diagram <path to diagram>

Now you can generate code

.. code:: shell

    $ python manage.py generate --diagram <path to diagram>

Here system will ask you what you want to generate for your app.

If you generated api you have to add app urls to urls.py:

.. code:: python

    urlpatterns = [
      path('api/', include('products.api.urls')),
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

-  For support Rest API doc add this part to your urls.py

.. code:: python

    from rest_framework.permissions import AllowAny
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Rest API Doc",
            default_version='v1',
            description="Auto Generated API Docs",
            license=openapi.License(name="S.A.G.E License"),
        ),
        public=True,
        permission_classes=(AllowAny,),
    )

    urlpatterns = [
        path('api/doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
    ]

-  Rest API documentation is available at ``localhost:8000/api/doc/``

Contribute
----------

Run project tests before starting to develop

-  ``products`` app is required for running tests

.. code:: shell

    $ python manage.py startapp products

.. code:: python

    INSTALLED_APPS = [
      'products',
    ]

-  you have to generate everything for this app

-  diagram file is available here:
   `Diagram <sage_painless/tests/diagrams/product_diagram.json>`__

.. code:: shell

    $ python manage.py generate --diagram sage_painless/tests/diagrams/product_diagram.json

-  run tests

.. code:: shell

    $ python manage.py test sage_painless

Team
----

+-----------------------------------------------------------------+---------------------------------------------------------+
| |sepehr|                                                        |                            |mehran|                     |
+=================================================================+=========================================================+
| `Sepehr Akbarazadeh <https://github.com/sepehr-akbarzadeh>`__   | `Mehran Rahmanzadeh <https://github.com/mrhnz>`__       |
+-----------------------------------------------------------------+---------------------------------------------------------+

.. |SageTeam| image:: https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_sage.png?raw=true
            :alt: SageTeam
.. |PyPI release| image:: https://img.shields.io/pypi/v/django-sage-painless
            :alt: django-sage-painless
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/django-sage-painless
            :alt: django-sage-painless
.. |Supported Django versions| image:: https://img.shields.io/pypi/djversions/django-sage-painless
            :alt: django-sage-painless
.. |Documentation| image:: https://img.shields.io/readthedocs/django-sage-painless
            :alt: django-sage-painless
.. |Build| image:: https://img.shields.io/appveyor/build/mrhnz/django-sage-painless
            :alt: django-sage-painless
.. |sepehr| image:: https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/sepehr.jpeg?raw=true
            :height: 230px
            :width: 230px
            :alt: Sepehr Akbarzadeh
.. |mehran| image:: https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/mehran.png?raw=true
            :height: 340px
            :width: 225px
            :alt: Mehran Rahmanzadeh
