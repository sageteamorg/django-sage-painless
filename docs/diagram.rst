Diagram
===========

Template
----------------

Diagram is a json file that contains database tables, settings for admin panel and API configs
It is the only thing you need to generate a whole project

There are 2 types of diagram:

1. generate diagram (for generating Django apps)
2. [NEW] deploy diagram (for generating deploy configs like docker, gunicorn, uwsgi, etc)

[NEW]: You can also use `encryption` capability in diagram. Example:

.. code:: python

    "title": {
        "type": "character",
        "max_length": 255,
        "unique": true,
        "encrypt": true
      }

[NEW]: You can also use `streaming` capability in videos. Example:

.. code:: python

    "movie": {
        "type": "video",
        "upload_to": "movies",
        "stream": true
      }

It will add a new api to your project with `/stream` endpoint that gets video path in url like:

`localhost:8000/api/stream?path=<video_path>`

And it will stream it chunk by chunk.

the template of the diagram is something like this:

.. code:: python

    {
    "apps": {
      "ecommerce": {
       "models": {
        "Category": {
          "fields": {
              "title": {
                "type": "character",
                "max_length": 255,
                "unique": true
              },
              "created": {
                "type": "datetime",
                "auto_now_add": true
              },
              "modified": {
                "type": "datetime",
                "auto_now": true
              }
            },
            "admin": {
              "list_display": ["title", "created", "modified"],
              "list_filter": ["created", "modified"],
              "search_fields": ["title"]
            },
            "api": {
              "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"]
            }
          },
          "Product": {
            "fields": {
              "title": {
                "type": "character",
                "max_length": 255
              },
              "description": {
                "type": "character",
                "max_length": 255
              },
              "price": {
                "type": "integer"
              },
              "category": {
                "type": "fk",
                "to": "Category",
                "related_name": "'products'",
                "on_delete": "CASCADE"
              },
              "created": {
                "type": "datetime",
                "auto_now_add": true
              },
              "modified": {
                "type": "datetime",
                "auto_now": true
              }
            },
            "admin": {
              "list_display": ["title", "price", "category"],
              "list_filter": ["created", "modified"],
              "search_fields": ["title", "description"],
              "raw_id_fields": ["category"]
            }
          },
        "Discount": {
          "fields": {
            "product": {
              "type": "fk",
              "to": "Product",
              "related_name": "'discounts'",
              "on_delete": "CASCADE"
            },
            "discount": {
              "type": "integer"
            },
            "created": {
              "type": "datetime",
              "auto_now_add": true
            },
            "modified": {
              "type": "datetime",
              "auto_now": true
            }
          },
          "admin": {
            "list_display": ["discount", "product", "created", "modified"],
            "list_filter": ["created", "modified"],
            "raw_id_fields": ["product"]
          }
        }
      }
    }
  }
}

field types are:

==========  =======================
   Type             Django
==========  =======================
character   CharField
integer     IntegerField
float       FloatField
datetime    DateTimeField
date        DateField
time        TimeField
text        TextField
fk          ForeignKey
one2one     OneToOneField
m2m         ManyToManyField
image       ImageField
file        FileField
video       FileField
bool        BooleanField
slug        SlugField
==========  =======================

in admin you can set:

======================  =======================
      Option             Input
======================  =======================
fields                  list of strings
fieldsets               list
ordering                list of strings
readonly_fields         list of strings
exclude                 list of strings
list_display            list of strings
list_display_links      list of strings
list_filter             list of strings
list_editable           list of strings
search_fields           list of strings
filter_horizontal       list of strings
filter_vertical         list of strings
raw_id_fields           list of strings
has_add_permission        boolean
has_change_permission     boolean
has_delete_permission     boolean
======================  =======================

in api you can set:

======================  =======================
      Option             Input
======================  =======================
methods                 list of strings (Not case sensitive)
======================  =======================

Examples
----------------

example 1 (generate diagram):

2 apps (ecommerce & discount)

.. code:: json

    {
      "apps": {
        "ecommerce": {
          "models": {
            "Category": {
              "fields": {
                "title": {
                  "type": "character",
                  "max_length": 255,
                  "unique": true
                },
                "created": {
                  "type": "datetime",
                  "auto_now_add": true
                },
                "modified": {
                  "type": "datetime",
                  "auto_now": true
                }
              },
              "admin": {
                "list_display": [
                  "title",
                  "created",
                  "modified"
                ],
                "list_filter": [
                  "created",
                  "modified"
                ],
                "search_fields": [
                  "title"
                ]
              },
              "api": {
                "methods": [
                  "GET",
                  "POST",
                  "PUT",
                  "PATCH",
                  "DELETE"
                ]
              }
            },
            "Product": {
              "fields": {
                "title": {
                  "type": "character",
                  "max_length": 255
                },
                "description": {
                  "type": "character",
                  "max_length": 255
                },
                "price": {
                  "type": "integer"
                },
                "category": {
                  "type": "fk",
                  "to": "Category",
                  "related_name": "'products'",
                  "on_delete": "CASCADE"
                },
                "created": {
                  "type": "datetime",
                  "auto_now_add": true
                },
                "modified": {
                  "type": "datetime",
                  "auto_now": true
                }
              },
              "admin": {
                "list_display": [
                  "title",
                  "price",
                  "category"
                ],
                "list_filter": [
                  "created",
                  "modified"
                ],
                "search_fields": [
                  "title",
                  "description"
                ],
                "raw_id_fields": [
                  "category"
                ]
              }
            }
          }
        },
        "discount": {
          "models": {
            "Discount": {
              "fields": {
                "product": {
                  "type": "fk",
                  "to": "Product",
                  "related_name": "'discounts'",
                  "on_delete": "CASCADE"
                },
                "discount": {
                  "type": "integer"
                },
                "created": {
                  "type": "datetime",
                  "auto_now_add": true
                },
                "modified": {
                  "type": "datetime",
                  "auto_now": true
                }
              },
              "admin": {
                "list_display": [
                  "discount",
                  "product",
                  "created",
                  "modified"
                ],
                "list_filter": [
                  "created",
                  "modified"
                ],
                "raw_id_fields": [
                  "product"
                ]
              }
            }
          }
        }
      }
    }


example 2 (generate diagram):

1 app (articles)

.. code:: json

    {
      "apps": {
        "articles": {
          "models": {
            "Article": {
              "fields": {
                "title": {
                  "type": "character",
                  "max_length": 120
                },
                "body": {
                  "type": "character",
                  "max_length": 255
                },
                "slug": {
                  "type": "slug",
                  "max_length": 255,
                  "unique": true
                },
                "created": {
                  "type": "datetime",
                  "auto_now_add": true
                },
                "publish": {
                  "type": "datetime",
                  "null": true,
                  "blank": true
                },
                "updated": {
                  "type": "datetime",
                  "auto_now": true
                },
                "options": {
                  "type": "character",
                  "max_length": 2,
                  "choices": [
                    [
                      "dr",
                      "Draft"
                    ],
                    [
                      "pb",
                      "public"
                    ],
                    [
                      "sn",
                      "soon"
                    ]
                  ]
                }
              },
              "admin": {
                "list_display": [
                  "title",
                  "created",
                  "updated"
                ],
                "list_filter": [
                  "created",
                  "updated",
                  "options"
                ],
                "search_fields": [
                  "title",
                  "body"
                ]
              },
              "api": {
                "methods": [
                  "get",
                  "post"
                ]
              }
            }
          }
        }
      }
    }

[NEW] example 3 (deploy diagram):

.. code:: json

    {
      "deploy": {
        "docker": {
          "db_image": "postgres",
          "db_name": "products",
          "db_user": "postgres",
          "db_pass": "postgres1234",
          "redis": true,
          "rabbitmq": false
        },
        "gunicorn": {
          "project_name": "kernel",
          "worker_class": "sync",
          "worker_connections": 5000,
          "workers": 5,
          "accesslog": "/var/log/gunicorn/gunicorn-access.log",
          "errorlog": "/var/log/gunicorn/gunicorn-error.log",
          "reload": true
        },
        "uwsgi": {
          "chdir": "/src/kernel",
          "home": "/src/venv",
          "module": "kernel.wsgi",
          "master": true,
          "pidfile": "/tmp/project-master.pid",
          "vacuum": true,
          "max-requests": 3000,
          "processes": 10,
          "daemonize": "/var/log/uwsgi/uwsgi.log"
        },
        "tox": {
          "version": "1.0.0",
          "description": "test project",
          "author": "SageTeam",
          "req_path": "requirements.txt"
        }
      }
    }