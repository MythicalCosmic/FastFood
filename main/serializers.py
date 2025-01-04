from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from rest_framework import serializers # type: ignore
from .models import *
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from django.contrib.auth.models import User, Group, Permission

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed({
                "ok": False,
                "error_code": "INVALID_CREDENTIALS",
                "message": "The provided credentials are incorrect or the account is inactive."
            })
        user = self.user
        data['username'] = getattr(self.user, 'username', None)
        data['role'] = user.groups.first().name if user.groups.exists() else None 
        data['permissions'] = list(user.get_all_permissions())
        data['superuser_status'] = user.is_superuser
        return data
    
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, many=True)
    user_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), required=False, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'is_active', 'is_staff', 'is_superuser', 'date_joined', 
                  'last_login', 'groups', 'user_permissions', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        user = User(**validated_data)
        print(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if groups:
            instance.groups.set(groups)
        if user_permissions:
            instance.user_permissions.set(user_permissions)

        return instance
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def create(self, validated_data):
        permissions = self.initial_data.get('permissions', [])
        group = Group.objects.create(name=validated_data['name'])
        group.permissions.set(permissions)
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        permissions = self.initial_data.get('permissions', None)
        if permissions is not None:
            instance.permissions.set(permissions)
        instance.save()
        return instance


