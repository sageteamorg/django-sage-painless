from django.apps import AppConfig


class UploadCenterConfig(AppConfig):
    name = 'upload_center'
    verbose_name = 'Upload Center'

    def ready(self):
        import upload_center.signals
