from django.contrib import admin

from upload_center.models import UserDiagramUpload


@admin.register(UserDiagramUpload)
class UserDiagramUploadAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'base_dir',
        'project_name',
        'app_name',
        'created',
        'modified',
    )

    list_filter = (
        'object_scope',
        'created',
        'modified'
    )
