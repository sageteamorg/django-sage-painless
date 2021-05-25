from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from django.core.validators import (
    FileExtensionValidator,
    MinLengthValidator,
    MaxLengthValidator
)

from .mixins import (
    DeletedAtMixin,
    TimeStampModelMixin
)
from .common import (
    UUIDBaseModel
)

from painless.utils.upload.path import (
    user_directory_path
)


class UserImageAltUpload(UUIDBaseModel, TimeStampModelMixin, DeletedAtMixin):
    image = models.ImageField(
        _("Avatar"),
        upload_to=user_directory_path,
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'jpg', 'jpeg', 'png'])]
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )
    width_field = models.PositiveSmallIntegerField(
        _("Width Field"),
        editable=False
    )
    height_field = models.PositiveSmallIntegerField(
        _("Height Field"),
        editable=False
    )

    SCOPES = (
        ('user', _('User')),
        ('service', _('service')),
        ('category', _('category')),
    )

    object_scope = models.CharField(
        max_length=10,
        choices=SCOPES
    )
    object_id = models.CharField(
        max_length=100
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name='images',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
