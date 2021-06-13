class Admin:

    def __init__(self):
        self.model = None
        self.list_display = None
        self.list_filter = None
        self.search_fields = None
        self.raw_id_fields = None
        self.filter_horizontal = None
        self.filter_vertical = None
        self.has_add_permission = True
        self.has_change_permission = True
        self.has_delete_permission = True
