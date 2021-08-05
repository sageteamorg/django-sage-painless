Usage
-----

For generating a whole project you just need a diagram. diagram is a
json file that contains information about database tables.

`you can find examples of diagram file
here <https://github.com/sageteam-org/django-sage-painless/tree/develop/sage_painless/docs/diagrams>`__

start to generate (it is required for development. you will run tests on
this app)

[NEW]: First validate the format of your diagram, It will raise errors if diagram format was incorrect.

.. code:: shell

    $ python manage.py validate_diagram --diagram <path to diagram>

Now you can generate code

.. code:: shell

    $ python manage.py generate --diagram <path to diagram>

You can generate deploy config files

.. code:: shell

    $ python manage.py deploy --diagram <path to deploy diagram>

You can generate docs files

.. code:: shell

    $ python manage.py docs --diagram <path to diagram>

Here system will ask you what you want to generate for your app.
Questions:

======================================================================  ==========================================================================
                            Question                                                       Description
======================================================================  ==========================================================================
Would you like to generate models.py(yes/no)?                           generates models.py from json diagram for your app
Would you like to generate admin.py(yes/no)?                            generates admin.py from admin settings in json diagram for your project
Would you like to generate serializers.py & views.py(yes/no)?           generates serializers.py and views.py in api directory for your project
Would you like to generate test for your project(yes/no)?               generates model test and api test for your project in tests directory
Would you like to add cache queryset support(yes/no)?                   it will cache queryset via redis in your views.py
======================================================================  ==========================================================================


If you generated api you have to add app urls to urls.py:

.. code:: python

    urlpatterns = [
      ...
      path('api/', include('products.api.urls')),
      ...
    ]

If you set cache support add CACHES to your settings:

.. code:: python

    REDIS_URL = 'redis://localhost:6379/'
    CACHES = {
        "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ['REDIS_URL'] if os.environ.get('REDIS_URL') else settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else 'redis://localhost:6379/'
        }
    }

If you have encrypted field in diagram:

- your database should be PostgreSQL
- you should install `pgcrypto` extension for PostgreSQL with this command

.. code:: shell

    $ sudo -u postgres psql <db_name>
    $ CREATE EXTENSION pgcrypto;

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
        ...
        path('api/doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
        ...
    ]

-  Rest API documentation is available at ``localhost:8000/api/doc/``
