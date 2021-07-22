# {{project_name}}

This is an auto-generated README.md for `{{project_name}}` project

- [Description](#description)
- [Detail](#detail)
- [Structure](#structure)
- [Getting Started](#getting-started)

## Description

- Write your own

## Detail

- Version: {{project_version}}
- Language: Python: {{django_version}}
- Framework: Django: {{py_version}}

Built-in Django Apps:

{% for app in built_in_apps %}
- {{app}}
{% endfor %}

Other Used Apps:

{% for app in installed_modules %}
- {{app}}
{% endfor %}

## Structure

{{project_name}} files structure

```shell
{% for line in structure %}
{{line}}
{% endfor %}
```

## Getting Started

{% if docker_support %}

### Docker

The project is dockerized for deployment.

- Change directory to root of your project and run:

```shell
$ docker-compose up -d --build
```

- Collect static files:

```shell
$ docker-compose exec <container_name> python manage.py collectstatic
```

- Test:

```shell
$ docker-compose exec <container_name> python manage.py check --deploy
$ docker-compose exec <container_name> python manage.py test
```

{% endif %}

### Django Server

- Before running Django project you must first create virtualenv.

``` shell
$ python{{py_version}} -m pip install virtualenv
$ python{{py_version}} -m virtualenv venv
```

- To activate virtualenvironment:

ubuntu:

```shell
$ source venv/bin/activate
```

windows:

```shell
$ venv\Scripts\activate.bat
```

- To deactivate vritualenvironment use:

``` shell
$ deactivate
```

- After activation must install all packages:
```shell
$ pip install -r requirements.txt
```

- Check your settings for db config and continue to create database:

``` sql
CREATE USER <you_user> WITH PASSWORD <you_password>;
CREATE DATABASE <db_name>;
ALTER ROLE <you_user> SET client_encoding TO 'utf8';
ALTER ROLE <you_user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <you_user> SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <you_user>;
```

- Run check command to connect db:

```shell
$ python manage.py check
```

- Create all database tables:

```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

- On deployment:

```shell
$ python manage.py collectstatic
$ python manage.py test
$ python manage.py check --deploy
```

#### Automatically generated with ❤️ by [django-sage-painless](https://github.com/sageteam-org/django-sage-painless)