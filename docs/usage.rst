Usage
-----

For generating a whole project you just need a diagram. diagram is a
json file that contains information about database tables.

`you can find examples of diagram file
here <https://github.com/sageteam-org/django-sage-painless/tree/develop/sage_painless/docs/diagrams>`__

start to generate (it is required for development. you will run tests on
this app)

.. code:: shell

    $ python manage.py generate --app products --diagram <path to diagram>

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
Would you like to dockerize your project(yes/no)?                       creates Dockerfile and docker-compose.yml for your project
======================================================================  ==========================================================================

If you chose to dockerize project:

======================================================================  ==========================================================================
                            Question                                                       Description
======================================================================  ==========================================================================
Please enter the version of your project(e.g 2.1):                      the version of your project in number
Please enter your project's database image(e.g postgres):               it can be one of docker images recommended `postgres`
Please enter database name:                                             your database name that set in django settings
Please enter database user username:                                    the database will create by this user
Please enter database user password:                                    password of user
Would you like to config redis server for your project(yes/no)?         if you want cache support `yes` else `no`
Would you like to config rabbitMQ for your project(yes/no)?             configs RabbitMQ in your docker environment
======================================================================  ==========================================================================

If you chose to config RabbitMQ:

======================================================================  ==========================================================================
                            Question                                                       Description
======================================================================  ==========================================================================
Please enter rabbitMQ user username:                                    RabbitMQ user username
Please enter rabbitMQ user password:                                    RabbitMQ user password
======================================================================  ==========================================================================

If you generated api you have to add app urls to urls.py:

.. code:: python

    urlpatterns = [
      ...
      path('api/', include('products.api.urls')),
      ...
    ]

If you set cache support but you did not dockerize project add CACHES to your settings:

.. code:: python

    REDIS_URL = 'redis://localhost:6379/'
    CACHES = {
        "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ['REDIS_URL'] if os.environ.get('REDIS_URL') else settings.REDIS_URL if hasattr(settings, 'REDIS_URL') else 'redis://localhost:6379/'
        }
    }

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
