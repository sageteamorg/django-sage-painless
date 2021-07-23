from sage_painless.classes.field import Field


class DiagramValidator:
    """validate diagram and raise errors"""
    APPS_KEYWORD = 'apps'
    MODELS_KEYWORD = 'models'
    ADMIN_KEYWORD = 'admin'
    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'
    LIST_DISPLAY_KEYWORD = 'list_display'
    LIST_EDITABLE_KEYWORD = 'list_editable'
    LIST_DISPLAY_LINKS_KEYWORD = 'list_display_links'
    LIST_FILTER_KEYWORD = 'list_filter'
    SEARCH_FIELDS_KEYWORD = 'search_fields'
    RAW_ID_FIELDS_KEYWORD = 'raw_id_fields'
    FILTER_VERTICAL_KEYWORD = 'filter_vertical'
    FILTER_HORIZONTAL_KEYWORD = 'filter_horizontal'
    EXCLUDE_KEYWORD = 'exclude'
    ORDERING_KEYWORD = 'ordering'
    READONLY_FIELDS_KEYWORD = 'readonly_fields'

    def __init__(self):
        """init"""
        pass

    def search_in_list_items(self, item, list_):
        """is item in list_ item"""
        item_parts = item.split('__')
        search_item = item_parts[0]
        for item_ in list_:
            if search_item in item_:
                return True

        return False

    def validate_field_type(self, diagram):
        """validate fields
        `type` should be set
        check type is in allowed types
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                for field_name in model_fields:
                    field_data = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                        model_name).get(self.FIELDS_KEYWORD).get(field_name)
                    if not field_data.get(self.TYPE_KEYWORD):
                        raise KeyError(f'key `type` is required in model `{model_name}` for field `{field_name}`')
                    if not field_data.get(self.TYPE_KEYWORD) in Field.field_types:
                        raise KeyError(
                            f'type `{field_data.get(self.TYPE_KEYWORD)}` is not allowed in model `{model_name}` for field `{field_name}`')

    def validate_field_attributes(self, diagram):
        """validate fields
        each field type has allowed attributes
        and required attributes
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                for field_name in model_fields:
                    field_data = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                        model_name).get(self.FIELDS_KEYWORD).get(field_name)
                    field_required_attrs = Field.field_types.get(field_data.get(self.TYPE_KEYWORD)).get('required')
                    field_allowed_attrs = Field.field_types.get(field_data.get(self.TYPE_KEYWORD)).get('allowed')
                    for field_attr in field_data:
                        if field_attr not in field_allowed_attrs:
                            raise KeyError(
                                f'attribute `{field_attr}` is not allowed in model `{model_name}` for field `{field_name}` ')
                    for required_attr in field_required_attrs:
                        if required_attr not in field_data:
                            raise KeyError(
                                f'attribute `{required_attr}` is required in model `{model_name}` for field `{field_name}`')

    def validate_apps_key(self, diagram):
        """validate diagram
        diagram should has `apps` key
        """
        if not diagram.get(self.APPS_KEYWORD):
            raise KeyError(f'key `{self.APPS_KEYWORD}` is required in diagram')

    def validate_admin_list_display(self, diagram):
        """validate admin
        field names in `list_display` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.LIST_DISPLAY_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in list_display of model `{model_name}` does not exists')

    def validate_admin_list_display_links(self, diagram):
        """validate admin
        field names in `list_display_links` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.LIST_DISPLAY_LINKS_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in list_display_links of model `{model_name}` does not exists')

    def validate_admin_list_editable(self, diagram):
        """validate admin
        field names in `list_editable` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.LIST_EDITABLE_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in list_editable of model `{model_name}` does not exists')

    def validate_admin_readonly_fields(self, diagram):
        """validate admin
        field names in `readonly_fields` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.READONLY_FIELDS_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in readonly_fields of model `{model_name}` does not exists')

    def validate_admin_ordering(self, diagram):
        """validate admin
        field names in `ordering` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.ORDERING_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in ordering of model `{model_name}` does not exists')

    def validate_admin_list_filter(self, diagram):
        """validate admin
        field names in `list_filter` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.LIST_FILTER_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in list_filter of model `{model_name}` does not exists')

    def validate_admin_search_fields(self, diagram):
        """validate admin
        field names in `search_fields` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.SEARCH_FIELDS_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in search_fields of model `{model_name}` does not exists')

    def validate_admin_raw_id_fields(self, diagram):
        """validate admin
        field names in `raw_id_fields` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.RAW_ID_FIELDS_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in raw_id_fields of model `{model_name}` does not exists')

    def validate_admin_filter_vertical(self, diagram):
        """validate admin
        field names in `filter_vertical` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.FILTER_VERTICAL_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in filter_vertical of model `{model_name}` does not exists')

    def validate_admin_filter_horizontal(self, diagram):
        """validate admin
        field names in `filter_horizontal` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.FILTER_HORIZONTAL_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in filter_horizontal of model `{model_name}` does not exists')

    def validate_admin_exclude(self, diagram):
        """validate admin
        field names in `exclude` should be in model fields
        """
        for app_name in diagram.get(self.APPS_KEYWORD):
            app_models = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD)
            for model_name in app_models:
                model_admin = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(model_name).get(
                    self.ADMIN_KEYWORD)
                model_fields = diagram.get(self.APPS_KEYWORD).get(app_name).get(self.MODELS_KEYWORD).get(
                    model_name).get(self.FIELDS_KEYWORD)
                if model_admin:
                    list_display = model_admin.get(self.EXCLUDE_KEYWORD)
                    if list_display:
                        for field in list_display:
                            if not self.search_in_list_items(field, model_fields):
                                raise KeyError(
                                    f'field `{field}` in exclude of model `{model_name}` does not exists')

    def validate_all(self, diagram):
        """validate diagram with all conditions"""
        self.validate_field_type(diagram)
        self.validate_field_attributes(diagram)
        self.validate_apps_key(diagram)
        self.validate_admin_list_filter(diagram)
        self.validate_admin_list_display(diagram)
        self.validate_admin_list_editable(diagram)
        self.validate_admin_filter_horizontal(diagram)
        self.validate_admin_filter_vertical(diagram)
        self.validate_admin_list_display_links(diagram)
        self.validate_admin_exclude(diagram)
        self.validate_admin_ordering(diagram)
        self.validate_admin_raw_id_fields(diagram)
        self.validate_admin_search_fields(diagram)
