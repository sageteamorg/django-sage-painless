"""
Auto Generated models.py
You may need to change some parts
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):
    """
    User Model
    Auto generated
    """

    username = models.CharField(
        unique=True,
        max_length=255,
        blank=False,
    )

    password = models.CharField(
        max_length=255,
        blank=False,
    )

    first_name = models.CharField(
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    last_login = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"User"  # you may change this section

    class Meta:
        verbose_name = _("User")  # auto generated verbose_name
        verbose_name_plural = _("Users")


class Profile(models.Model):
    """
    Profile Model
    Auto generated
    """

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    image = models.ImageField(
        blank=True,
    )

    def __str__(self):
        return f"Profile"  # you may change this section

    class Meta:
        verbose_name = _("Profile")  # auto generated verbose_name
        verbose_name_plural = _("Profiles")
