import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from painless.utils.regex.patterns import PERSIAN_PHONE_NUMBER_PATTERN

from django.utils.translation import ugettext_lazy as _

########
PHONE_NUMBER_ERROR_MSG = _("please enter a valid phone_number. e.g. 09xx xxx xxxxx")
########

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        pattern = re.compile(PERSIAN_PHONE_NUMBER_PATTERN)
        if not pattern.match(value):
            raise serializers.ValidationError(PHONE_NUMBER_ERROR_MSG)
        return value

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

class ResetPasswordSerializer(PhoneNumberSerializer):
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        if not len(value) == 6:
            raise serializers.ValidationError("Invalid Token.")

        return value
