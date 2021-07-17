Diagram
===========

Template
----------------

Diagram is a json file that contains database tables and settings for admin panel
it is the only thing that you need to generate a whole project

the template of the diagram is something like this:

.. code:: python

    {
      "Category": { # table name
        "fields": {
          "title": {  # field name
            "type": "character", # field type
            "max_length": 255, # field arguments
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
        "admin": { # django admin settings
          "list_display": ["title", "created", "modified"],
          "list_filter": ["created", "modified"],
          "search_fields": ["title"]
        },
        "api": { # API settings (default is all model mixins)
          "methods": ["get", "post"]
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

.. code:: json

    {
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
        "api": { # API settings
          "methods": ["get"]
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
        },
        "api": { # API settings
          "methods": ["get"]
        }
      },
      "Discount": {
        "fields": {
          "product": {
            "type": "one2one",
            "to": "Product",
            "related_name": "'discounts'",
            "on_delete": "CASCADE"
          },
          "discount": {
            "type": "integer",
            "default": 0
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
        },
        "api": { # API settings
          "methods": ["get"]
        }
      }
    }


example 2:

.. code:: json

    {
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
            "choices": [["dr", "Draft"], ["pb", "public"], ["sn", "soon"]]
          }
        },
        "admin": {
          "list_display": ["title", "created", "updated"],
          "list_filter": ["created", "updated", "options"],
          "search_fields": ["title", "body"]
        },
        "api": { # API settings
          "methods": ["get", "post"]
        }
      }
    }