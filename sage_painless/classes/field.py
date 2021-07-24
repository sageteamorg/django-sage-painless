class Attribute:
    """Required Field object that contains `key` and `value`"""

    def __init__(self):
        """init"""
        self.key = None
        self.value = None

    def set_attr(self, attr_key, attr_value):
        """set `key` and `value`"""
        self.key = attr_key
        self.value = attr_value


class Validator:
    """Validator attribute for Field"""

    def __init__(self):
        """init"""
        self.func = None
        self.arg = None

    def set_validator(self, func, arg):
        """set `func` and `kwargs`"""
        self.func = func
        self.arg = arg


class Field:
    """Field object that contains attributes of a django model field"""

    def __init__(self):
        """init"""
        self.name = None
        self.type = None
        self.encrypted: bool = False
        self.stream: bool = False
        self.attrs = list()
        self.validators = list()

    field_types = {
        'character': {
            'type': 'CharField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': ['max_length']
        },
        'integer': {
            'type': 'IntegerField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': []
        },
        'float': {
            'type': 'FloatField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': []
        },
        'datetime': {
            'type': 'DateTimeField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'auto_now', 'auto_now_add', 'auto_now_created'],
            'required': []
        },
        'date': {
            'type': 'DateField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'auto_now', 'auto_now_add', 'auto_now_created'],
            'required': []
        },
        'time': {
            'type': 'TimeField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date', 'choices',
                'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'auto_now', 'auto_now_add', 'auto_now_created'],
            'required': []
        },
        'text': {
            'type': 'TextField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': []
        },
        'fk': {
            'type': 'ForeignKey',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'to', 'related_name', 'on_delete'],
            'required': ['to', 'on_delete']
        },
        'one2one': {
            'type': 'OneToOneField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'to', 'related_name'],
            'required': ['to']
        },
        'm2m': {
            'type': 'ManyToManyField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'to', 'related_name'],
            'required': ['to']
        },
        'image': {
            'type': 'ImageField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'upload_to'],
            'required': []
        },
        'video': {
            'type': 'FileField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'upload_to', 'stream'],
            'required': []
        },
        'file': {
            'type': 'FileField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages', 'upload_to'],
            'required': []
        },
        'bool': {
            'type': 'BooleanField',
            'allowed': [
                'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': []
        },
        'slug': {
            'type': 'SlugField',
            'allowed': [
                'max_length', 'default', 'null', 'blank', 'validators', 'encrypt', 'unique', 'type', 'verbose_name',
                'name', 'primary_key', 'db_index', 'rel', 'editable', 'serialize', 'unique_for_date',
                'unique_for_month', 'unique_for_year', 'choices', 'help_text', 'db_column', 'db_tablespace',
                'error_messages'],
            'required': []
        }
    }

    def set_type(self, field_type):
        """Set field type based on `field_types` and required_attrs"""
        field = self.field_types.get(field_type)
        if field:
            self.type = field.get('type')
            message = True, 'Applied Successfully'
        else:
            message = False, 'Field Not Defined'

        return message

    def add_attribute(self, key, value):
        """Add attribute to Field"""
        attr = Attribute()
        attr.set_attr(key, value)
        self.attrs.append(attr)
        return True

    def get_attribute(self, key):
        """Get attribute from field"""
        for attr in self.attrs:
            if attr.key == key:
                return attr.value

        return 'Not defined'

    def add_validator(self, func, arg):
        """Add validator to Field"""
        validator = Validator()
        validator.set_validator(func, arg)
        self.validators.append(validator)
