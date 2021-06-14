Contribute
===========

Project Detail
--------------

You can find all technologies we used in our project into these files:

- Version: 1.0.0
- Frameworks: Django 3.2.4
- Libraries:
    - Django rest framework 3.12.4
    - Jinja2 3.0.1
- Language: Python 3.9.4

Git Rules
---------

Sage team Git Rules Policy is available here:

-  `Sage Git
   Policy <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`__

Development
-----------

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
   `Diagram <https://github.com/sageteam-org/django-sage-painless/blob/develop/sage_painless/docs/diagrams/product_diagram.json>`__

.. code:: shell

    $ python manage.py generate --app products --diagram sage_painless/tests/diagrams/product_diagram.json

-  run tests

.. code:: shell

    $ python manage.py test sage_painless

