class Model:
    """
    Model object that contains `name` and `fields` of model
    """

    name = None
    fields = []

    def has_one_to_one(self):
        """
        model has one2one field
        """
        for field in self.fields:
            if field.type == 'OneToOneField':
                return True

        return False

    @property
    def verbose_name(self):
        """
        create model `verbose_name`
        """
        return self.name.capitalize() if self.name else 'Not Defined'

    @property
    def verbose_name_plural(self):
        """
        create model `verbose_name_plural`
        """
        if self.name:
            result = self.name.capitalize()
            if result[-1] == 's':
                result = f'{result}es'
            else:
                result = f'{result}s'
        else:
            result = 'Not Defined'

        return result

    @property
    def get_str(self):
        """
        return `__str__` value for model
        """
        return self.name
