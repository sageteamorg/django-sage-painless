FAQ
===========

**What is code generator?**
--------------------------------

A code generator is a tool or resource that generates a particular sort of code or computer programming language. This has many specific meanings in the world of IT, many of them related to the sometimes complex processes of converting human programming syntax to the machine language that can be read by a computing system.One of the most common and conventional uses of the term “code generator” involves other resources or tools that help to turn out specific kinds of code. For example, some homemade or open source code generators can generate classes and methods for easier or more convenient computer programming. This type of resource might also be called a component generator.

**What is django-sage-painless?**
------------------------------------------------

The django-sage-painless is a valuable package based on Django Web Framework & Django Rest Framework for high-level and rapid web development. The introduced package generates Django applications. After completing many projects, we concluded that any basic project and essential part is its database structure. You can give the database schema in this package and get some parts of the Django application, such as API, models, admin, signals, model cache, setting configuration, mixins, etc. All of these capabilities come with a unit test. So you no longer have to worry about the simple parts of Django, and now you can write your advanced services in Django. Django-sage-painless dramatically speeds up the initial development of the project in Django. However, we intend to make it possible to use it in projects that are in progress. But the reality now is that we have made Django a quick start. We used the name painless instead of the Django code generator because this package allows you to reach your goals with less effort.

**Why should we use this package?**
------------------------------------------------

One of the most important reasons to use this package is to speed up the development of Django applications. Then, another important reason is that you can use many features with this package if you want. Therefore, you DO NOT have to use all the features of the generator.

**What are the main features of the package?**
------------------------------------------------

- Generate models based on your defined diagram
- Support database relationships: [one-to-one] [one-to-many] [many-to-many]
- Generate cache mixin to your models (OPTIONAL)
- Generate model test
- Generate signals (if you use one-to-one relationship)
- Generate rest framework API endpoints (OPTIONAL)
- Generate rest framework documentation (OPTIONAL)
- Generate API URLs (if request for API)
- Generate API test
- Generate admin via filter and search capability (OPTIONAL)
- Generate setting configuration of (Redis, RabbitMQ, Celery, etc. OPTIONAL)
- Generate docker compose file, Dockerfile and related documentation (OPTIONAL)

**Why don't we produce the whole Django project?**
----------------------------------------------------------------

Based on this question, we took a new attitude was taken in the package. One of the important issues in package design is that it is scalable and compatible with projects that are under development. That's why we decided to automate only the apps according to the project design model instead of producing a complete Django project. Therefore, anyone can use this package in the middle of their startup development and release their new features faster than before.

**How to learn to create a diagram?**
------------------------------------------------

In the example section, we have taught all the sections related to Digram.

**How does the cache algorithm work?**
------------------------------------------------

Caching algorithm works in such a way that once your data is loaded, it is cached in Redis, and there is no need to query the database again. We have also designed the algorithm like that if your data in the database changes, cached data will be deleted automatically from Redis.
