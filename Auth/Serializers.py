from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password', 'is_active']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user