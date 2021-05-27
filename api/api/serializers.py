from rest_framework.serializers import ModelSerializer

from api.models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'last_login',

        ]


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'user',
            'description',
            'image',

        ]
