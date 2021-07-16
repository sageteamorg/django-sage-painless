# Django Sage Painless
#### django-sage-painless is a useful package based on Django Web Framework & Django Rest Framework for high-level and rapid web development.

##### The Latest version of [django-sage-painless](https://django-sage-painless.readthedocs.io/) documentation

![SageTeam](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_sage.png?raw=true "SageTeam")
![PyPI release](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_pypi_0.0.8.png?raw=true "django-sage-painless")
![Supported Python versions](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_python-02.png?raw=true "django-sage-painless")
![Supported Django versions](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_django.png?raw=true "django-sage-painless")
![Documentation](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_docs.png?raw=true "django-sage-painless")
![Test](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_test.png?raw=true "django-sage-painless")

- [Project Detail](#project-detail)
- [Git Rules](#git-rules)
- [Get Started](#getting-started)
- [Usage](#usage)
- [Contribute](#contribute)

## Project Detail

You can find all technologies we used in our project into these files:
* Version: 1.0.0
* Frameworks: 
  - Django 3.2.4
* Libraries:
  - Django rest framework 3.12.4
  - Jinja2 3.0.1
* Language: Python 3.9.4

## Git Rules

Sage team Git Rules Policy is available here:

- [Sage Git Policy](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

## Getting Started

Before creating django project you must first create virtualenv.

``` shell
$ python3.9 -m pip install virtualenv
$ python3.9 -m virtualenv venv
```

To activate virtualenvironment in ubuntu:

```shell
$ source venv/bin/activate
```

To deactive vritualenvironment use:

``` shell
$ deactivate
```

## Start Project

First create a Django project

```shell
$ mkdir GeneratorTutorials
$ cd GeneratorTutorials
$ django-admin startproject kernel .
```

Next we have to create an sample app that we want to generate code for it
(it is required for development. you will run tests on this app)

```shell
$ python manage.py startapp products
```

Now we have to add 'products' to INSTALLED_APPS in settings.py

```python
INSTALLED_APPS = [
  'products',
]
```

## Install Generator

First install package

```shell
$ pip install django-sage-painless
```

Then add 'sage_painless' to INSTALLED_APPS in settings.py

These apps should be in your INSTALLED_APPS:

- 'rest_framework'
- 'drf_yasg'
- 'django_seed'

```python
INSTALLED_APPS = [
  'sage_painless',
  'rest_framework',
  'drf_yasg',
  'django_seed',
]
```

## Usage

For generating a whole project you just need a diagram.
diagram is a json file that contains information about database tables.

[you can find examples of diagram file here](sage_painless/docs/diagrams)

start to generate
(it is required for development. you will run tests on this app)

```shell
$ python manage.py generate --app products --diagram <path to diagram>
```

Here system will ask you what you want to generate for your app.

If you generated api you have to add app urls to urls.py:

```python
urlpatterns = [
  path('api/', include('products.api.urls')),
]
```

- You have to migrate your new models

```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

- You can run tests for your app

```shell
$ python manage.py test products
```

- Django run server

```shell
$ python manage.py runserver
```
- Rest API documentation is available at `localhost:8000/api/doc/`
  
- For support Rest API doc add this part to your urls.py

```python
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
```

- Rest API documentation is available at `localhost:8000/api/doc/`

## Contribute

Run project tests before starting to develop

- `products` app is required for running tests

```shell
$ python manage.py startapp products
```

```python
INSTALLED_APPS = [
  'products',
]
```
- you have to generate everything for this app
  
- diagram file is available here: [Diagram](sage_painless/tests/diagrams/product_diagram.json)

```shell
$ python manage.py generate --app products --diagram sage_painless/tests/diagrams/product_diagram.json
```

- run tests

```shell
$ python manage.py test sage_painless
```

## Team
| [<img src="https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/sepehr.jpeg?raw=true" width="230px" height="230px" alt="Sepehr Akbarzadeh">](https://github.com/sepehr-akbarzadeh) | [<img src="https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/mehran.png?raw=true" width="225px" height="340px" alt="Mehran Rahmanzadeh">](https://github.com/mrhnz) |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Sepehr Akbarazadeh](https://github.com/sepehr-akbarzadeh)                                                                                                             | [Mehran Rahmanzadeh](https://github.com/mrhnz)                                                                                                       |