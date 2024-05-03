from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import User
from .Serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

class IsAdminOrReadOnly(IsAdminUser):
    """
    Permission class that allows admin users to perform any action,
    and allows read-only access to non-admin users.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return super().has_permission(request, view)
    

class UserListView(APIView):
    """
    List all users or create a new user.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


