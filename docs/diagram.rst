Diagram
===========

Template
----------------

Diagram is a json file that contains database tables, settings for admin panel and API configs
It is the only thing you need to generate a whole project

[NEW]: You can also use `encryption` capability in diagram. Example:

.. code:: python

    "title": {
        "type": "character",
        "max_length": 255,
        "unique": true,
        "encrypt": true
      }

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
text        TextField
fk          ForeignKey
one2one     OneToOneField
m2m         ManyToManyField
image       ImageField
file        FileField
bool        BooleanField
slug        SlugField
==========  =======================

in admin you can set:

======================  =======================
      Option             Input
======================  =======================
list_display            list of strings
list_filter             list of strings
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
methods                 list of strings
======================  =======================

Examples
----------------

example 1:

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


example 2:

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