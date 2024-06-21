from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer, ProfileImageUploadSerializer, LoginSerializer, SignUpSerializer


class AuthViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []

    @swagger_auto_schema(request_body=SignUpSerializer)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(email=request.data['email'])
            token = Token.objects.create(user=user)
            return Response(data={"token": token.key},status=status.HTTP_201_CREATED)
        else:
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LoginSerializer)
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CustomUserSerializer)
    @action(detail=False, methods=['put'])
    def update_info(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='post',
                         request_body=ProfileImageUploadSerializer,
                         responses={200: 'photo upload successful'}
                         )
    @action(detail=False, methods=['post'], parser_classes=[FormParser, MultiPartParser])
    def upload_photo(self, request):
        user = request.user
        serializer = ProfileImageUploadSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def deactivate(self, request, pk=None):
        user = request.user
        user.perform_destroy()
        return Response(status=status.HTTP_200_OK)
