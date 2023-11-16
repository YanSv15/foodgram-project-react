from rest_framework import viewsets
from django.contrib.auth import get_user_model

from users import serializers


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        pass


class FollowViewSet(viewsets.ModelViewSet):
    pass
