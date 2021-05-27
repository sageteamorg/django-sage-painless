from rest_framework.viewsets import ModelViewSet

from api.models import *
from api.api.serializers import *


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
