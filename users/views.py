from rest_framework import viewsets

from .models import User
from .permissions import IsSelfOrReadOnly, IsAdmin
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrReadOnly, IsAdmin]

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [IsAdmin]
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            self.permission_classes = [IsSelfOrReadOnly]
        if self.action in ['create']:
            self.permission_classes = []
        return super().get_permissions()