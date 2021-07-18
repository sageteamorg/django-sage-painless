.. django-sage-painless documentation master file, created by
   sphinx-quickstart on Mon Jun 14 13:15:46 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-sage-painless's documentation!
================================================

.. |br| raw:: html

   <br />

.. image:: https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_sage.png?raw=true
   :target: https://sageteam.org/
   :alt: SageTeam

|br|

.. image:: https://img.shields.io/pypi/v/django-sage-painless
   :target: https://pypi.org/project/django-sage-painless/
   :alt: PyPI release

.. image:: https://img.shields.io/pypi/pyversions/django-sage-painless
   :target: https://pypi.org/project/django-sage-painless/
   :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/djversions/django-sage-painless
   :target: https://pypi.org/project/django-sage-painless/
   :alt: Supported Django versions

.. image:: https://img.shields.io/readthedocs/django-sage-painless
   :target: https://django-sage-painless.readthedocs.io/
   :alt: Documentation

|br|

This app supports the following combinations of Django and Python:

==========  =======================
  Django      Python
==========  =======================
3.1         3.7, 3.8, 3.9
3.2         3.7, 3.8, 3.9
==========  =======================


Functionality
-------------

painless creates django backend projects without developer coding

it can generate these parts:

- models.py
- admin.py
- serializers.py
- views.py
- urls.py
- tests
- api documentation
- Dockerfile
- docker-compose.yml

it also can config pro stuff in django:

- Redis cache
- RabbitMQ

Documentation
-------------

.. toctree::
   :maxdepth: 3

   quick_start
   usage
   diagram
   contribute
   faq

Issues
------

If you have questions or have trouble using the app please file a bug report at:

https://github.com/sageteam-org/django-sage-painless/issues



Indices and tables
==================

* :ref:`search`
