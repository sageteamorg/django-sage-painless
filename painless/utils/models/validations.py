from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _, ngettext_lazy
from django.core.validators import (
    BaseValidator, 
    RegexValidator
)
from django.core.files.images import get_image_dimensions

from painless.utils.regex.patterns import PERSIAN_PHONE_NUMBER_PATTERN

@deconstructible
class PersianPhoneNumberValidator(RegexValidator):
    regex = PERSIAN_PHONE_NUMBER_PATTERN
    message = _(
        'Enter a valid username(phone number). This value may contain only numbers'
    )
    flags = 0

@deconstructible
class DimensionValidator(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __call__(self, value):
        pic = value
        w, h = get_image_dimensions(pic)

        if not (w == self.width and h == self.height):
            raise ValidationError(
                _('Expected Dim: [ %(width)sw , %(height)sh ] But Actual Dim: [ %(w)sw , %(h)sh ].'),
                params={"width": self.width, "height": self.height, "w": w, "h": h}
            )

@deconstructible
class SquareDimension(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        pic = value
        w, h = get_image_dimensions(pic)

        if not (w == h):
            raise ValidationError(
                _('Width and Height must be equal (square image).')
            )

def validate_comma_seperator(value):
    if ',' not in value:
        raise ValidationError(
                _('%(value)s is not a comma-separated list.'),
                params={"value": value}
            )

def validate_placeholder(value):
    if '(---)' in value:
        raise ValidationError(
            _('%(value)s is not placeholder format.'),
            params={"value": value}
        )

def validate_(value):
    if '(---)' in value:
        raise ValidationError(
            _('%(value)s is not placeholder format.'),
            params={"value": value}
        )
