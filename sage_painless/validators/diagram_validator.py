"""
get diagram as input:

1. in encryption mode -> check db is postgres
2. in character -> check `max_length` is set [DONE]
3. in fk -> check `to` & `on_delete` is set [DONE]
4. in one2one -> check `to` is set [DONE]
5. in m2m -> check `to` is set [DONE]
6. check allowed attributes for each field type [DONE]
7. check required attributes for each field type [DONE]
8. check required keys for diagram json
9. check `type` is set in all fields [DONE]
10. check field type is allowed [DONE]
"""

from sage_painless.classes.field import Field


class DiagramValidator:
    """validate diagram and raise errors"""
    APPS_KEYWORD = 'apps'
    MODELS_KEYWORD = 'models'
    FIELDS_KEYWORD = 'fields'
    TYPE_KEYWORD = 'type'

    def __init__(self):
        """init"""
        pass

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
