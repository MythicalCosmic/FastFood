from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from rest_framework import serializers # type: ignore
from .models import *
from rest_framework.exceptions import AuthenticationFailed # type: ignore

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