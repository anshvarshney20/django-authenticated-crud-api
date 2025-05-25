from rest_framework import serializers
from .models import CRUD
from datetime import datetime
from django.contrib.auth import get_user_model 

User = get_user_model()

class CRUD_Serializers(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=200)
    message = serializers.CharField(required=True, allow_blank=False, max_length=1000)
    createdAt = serializers.DateTimeField(default=datetime.now)

    def create(self, validated_data):
        return CRUD.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user
# class CRUD_Serializers(serializers.ModelSerializer):
#     class Meta:
#         model = CRUD
#         fields = ['uid', 'title', 'message', 'createdAt']