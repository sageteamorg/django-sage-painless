import uuid
from django.db import models

from .mixins import (
    Sku_Mixin,
    TitleSlugLinkModelMixin,
    TimeStampModelMixin,
    DeletedAtMixin
)


class UUIDBaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        abstract = True


class TraditionalBaseModel(Sku_Mixin, TitleSlugLinkModelMixin, TimeStampModelMixin, DeletedAtMixin):
    class Meta:
        abstract = True
