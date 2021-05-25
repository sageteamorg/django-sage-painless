class AdminModel:
    """
    Admin generate Model class
    """
    def __init__(self):
        self.model_name = None
        self.model = None
        self.fields = None
        self.fk_fields = None
        self.m2m_fields = None
        self.char_fields = None

    def set_model_name(self, model_name):
        self.model_name = model_name
        return True

    def get_model_name(self):
        return self.model_name

    def set_model(self, model_class):
        self.model = model_class
        return True

    def get_model(self):
        return self.model

    def set_fields(self, fields: list):
        self.fields = fields
        return True

    def get_fields(self):
        return self.fields

    def set_fk_fields(self, fields: list):
        self.fk_fields = fields
        return True

    def get_fk_fields(self):
        return self.fk_fields

    def set_m2m_fields(self, fields: list):
        self.m2m_fields = fields
        return True

    def get_m2m_fields(self):
        return self.m2m_fields

    def set_char_fields(self, fields: list):
        self.char_fields = fields
        return True

    def get_char_fields(self):
        return self.char_fields
