"""
django-sage-painless - Model Class

:author: Mehran Rahmanzadeh (mrhnz13@gmail.com)
"""


class Model:
    """
    Model object that contains `name` and `fields` of model
    """

    name = None
    fields = []
    api_config = {}

    def has_one_to_one(self):
        """
        model has one2one field
        """
        for field in self.fields:
            if field.type == 'OneToOneField':
                return True

        return False

    @property
    def filter_fields(self):
        """return model filter patterns"""
        fields = list()
        for field in self.fields:
            if field.type in ['ForeignKey', 'OneToOneField', 'ManyToManyField']:
                fields.append(f'{field.name}__id')
            else:
                fields.append(field.name)
        return fields

    @property
    def search_fields(self):
        """return model search field patterns"""
        fields = list()
        for field in self.fields:
            if field.type in ['CharField', 'TextField', 'DateTimeField', 'DateField', 'TimeField', 'SlugField']:
                fields.append(field.name)
        return fields

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
            wordlist = []
            for char in self.name:
                wordlist.append(char)
            if self.name[len(self.name) - 1] == "y":
                wordlist[len(self.name) - 1] = "ies"
            else:
                wordlist.append("s")
            word = ""
            for i in wordlist:
                word += i
            return word
        else:
            return 'Not Defined'

    @property
    def get_str(self):
        """
        return `__str__` value for model
        """
        return self.name
