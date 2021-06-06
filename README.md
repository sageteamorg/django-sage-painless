# [Project Name]
#### [project name] is a useful package based on Django Web Framework & Django Rest Framework for high-level and rapid web development.
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
$ source venv\bin\activate
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

Next we have to create an app that we want to generate code for it
```shell
$ python manage.py startapp products
```
Now we have to add 'products' to INSTALLED_APPS in settings.py
```python
INSTALLED_APPS = [
  ...
  'products',
  ...
]
```

## Install Generator
First install package
```shell
$ pip install [project name]
```
Then add '[project name]' to INSTALLED_APPS in settings.py
```python
INSTALLED_APPS = [
  ...
  '[project name]',
  ...
]
```

## Usage
For generating a whole project you just need a diagram.
diagram is a json file that contains information about database tables.

[you can find examples of diagram file here](docs/diagrams)

start to generate
```shell
$ python manage.py generate --app products --diagram <path to diagram>
```

Here system will ask you what you want to generate for your app.

If you generated api you have to add app urls to urls.py:
```python
urlpatterns = [
  ...
  path('api/', include('products.api.urls')),
  ...
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





