from safedelete import DELETED_INVISIBLE
from safedelete.managers import SafeDeleteManager

class SafeDeleteManagerMixin(SafeDeleteManager):
    _safedelete_visibility = DELETED_INVISIBLE