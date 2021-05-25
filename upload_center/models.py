from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _

from painless.utils.models.mixins import SafeDeleteModelMixin, TimeStampModelMixin
from painless.utils.upload.path import date_directory_path


class UserDiagramUpload(SafeDeleteModelMixin, TimeStampModelMixin):
    SCOPES = (
        ('my_sql', _('MySQL')),
        ('postgres', _('Postgres')),
        ('sql_server', _('SQL Server'))
    )

    object_scope = models.CharField(
        _('Diagram Format'),
        max_length=10,
        choices=SCOPES,
        null=True,
        blank=True
    )

    diagram = models.FileField(
        _('Diagram File'),
        upload_to=date_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['sql', ])]
    )

    base_dir = models.CharField(
        _('Base Directory Name'),
        max_length=255
    )

    project_name = models.CharField(
        _('Project Name'),
        max_length=255
    )

    app_name = models.CharField(
        _('App Name'),
        max_length=255
    )

    model_support = models.BooleanField(
        _('Create Model'),
        default=True
    )

    admin_support = models.BooleanField(
        _('Create Admin'),
        default=True
    )

    api_support = models.BooleanField(
        _('Create API'),
        default=True
    )

    doc_support = models.BooleanField(
        _('Create Documentation'),
        default=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='diagrams',
        on_delete=models.SET_NULL,
        verbose_name=_('User'),
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user}: {self.object_scope}'