from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxLengthValidator, MinLengthValidator
from django.db import models

from painless.utils.models.common import UUIDBaseModel
from painless.utils.models.mixins import TimeStampModelMixin, VideoMP4_Mixin

from django.utils.translation import ugettext_lazy as _

from painless.utils.upload.path import date_directory_path


class ImageUploadModelMixin(UUIDBaseModel, TimeStampModelMixin):
    """
    Image upload model mixin
    """
    image = models.ImageField(
        _("Picture"),
        upload_to=date_directory_path,
        height_field='height',
        width_field='width',
        max_length=110,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'JPG', 'JPEG', 'PNG',
                'jpg', 'jpeg', 'png'
            ])
        ]
    )

    file_size = models.IntegerField(
        _('File Size'),
        null=True,
        blank=True,
        editable=False
    )

    file_name = models.CharField(
        _('File Name'),
        max_length=255,
        null=True,
        blank=True,
        editable=False
    )

    upload_time = models.PositiveSmallIntegerField(
        _('Upload Time'),
        null=True,
        blank=True,
        editable=False
    )

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=150,
        null=True,
        blank=True,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ]
    )

    width = models.PositiveSmallIntegerField(
        _("Width Field"),
        null=True,
        blank=True,
        editable=False
    )

    height = models.PositiveSmallIntegerField(
        _("Height Field"),
        null=True,
        blank=True,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name='images',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.file_size:
            self.file_size = self.image.size
        if not self.file_name:
            self.file_name = self.image.name
        if not self.upload_time:
            if hasattr(self.image, 'upload_time'):
                self.upload_time = self.image.upload_time
        super(ImageUploadModelMixin, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Image Upload')
        verbose_name_plural = _('Image Uploads')
        abstract = True


class VideoUploadModelMixin(UUIDBaseModel, TimeStampModelMixin, VideoMP4_Mixin):
    """
    Video upload model mixin
    """
    file_size = models.IntegerField(
        _('File Size'),
        null=True,
        blank=True,
        editable=False
    )

    file_name = models.CharField(
        _('File Name'),
        max_length=255,
        null=True,
        blank=True,
        editable=False
    )

    upload_time = models.PositiveSmallIntegerField(
        _('Upload Time'),
        null=True,
        blank=True,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name='videos',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.file_size:
            self.file_size = self.video.size
        if not self.file_name:
            self.file_name = self.video.name
        if not self.upload_time:
            if hasattr(self.video, 'upload_time'):
                self.upload_time = self.video.upload_time
        super(VideoUploadModelMixin, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Video Upload')
        verbose_name_plural = _('Video Uploads')
        abstract = True
