class Model:
    """
    Model object that contains `name` and `fields` of model
    """

    name = None
    fields = []

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
