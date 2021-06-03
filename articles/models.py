"""
Auto Generated models.py
You may need to change some parts
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    """
    Article Model
    Auto generated
    """

    title = models.CharField(
        max_length=120,

    )

    body = models.CharField(
        max_length=255,

    )

    slug = models.SlugField(
        max_length=255,
        unique=True,

    )

    created = models.DateTimeField(
        auto_now_add=True,

    )

    publish = models.DateTimeField(
        null=True,
        blank=True,

    )

    updated = models.DateTimeField(
        auto_now=True,

    )

    options = models.CharField(
        max_length=2,
        choices=[['dr', 'Draft'], ['pb', 'public'], ['sn', 'soon']],

    )

    def __str__(self):
        return f"Article"  # you may change this section

    class Meta:
        verbose_name = _("Article")  # auto generated verbose_name
        verbose_name_plural = _("Articles")
