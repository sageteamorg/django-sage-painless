from django.db.models.signals import post_save
from django.dispatch import receiver

from upload_center.models import UserDiagramUpload
from upload_center.services import Generator


@receiver(post_save, sender=UserDiagramUpload)
def save_diagram_upload(sender, instance, created, **kwargs):
    if created:
        generator = Generator(
            instance.diagram.path,
            instance.base_dir,
            instance.project_name,
            instance.app_name,
            instance.model_support,
            instance.admin_support,
            instance.api_support,
            instance.doc_support
        )
        generator.generate()
