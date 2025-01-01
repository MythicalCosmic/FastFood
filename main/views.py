from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from .models import *
from .serializers import *  
import jwt
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken # type: ignore
from datetime import datetime
from rest_framework.views import APIView # type: ignore


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')

        if access_token:
            try:
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                expires_in = int(decoded_token['exp'] - datetime.utcnow().timestamp()) 
                user_id = decoded_token.get('user_id')  
                username = response.data.get('username')
                user_role = response.data.get('role')
                user_permissions = response.data.get('permissions')
                superuser_status = response.data.get('superuser_status')
                if superuser_status:
                    response_data = {
                        'ok': True,
                        'message': 'Login successful',
                        'data': {
                            'user_data': {
                                'user_id': user_id,
                                'username': username,
                                'superuser_status': superuser_status
                            },  
                            'access_token': response.data['access'],
                            'token_type': 'Bearer',
                            'expires_in': expires_in 
                        }
                    }
                else:
                    response_data = {
                        'ok': True,
                        'message': 'Login successful',
                        'data': {
                            'user_data': {
                                'user_id': user_id,
                                'username': username,
                                'user_role': user_role,
                                'user_permissions': user_permissions,
                                'superuser_status': superuser_status
                            },  
                            'access_token': response.data['access'],
                            'token_type': 'Bearer',
                        '   expires_in': expires_in 
                        }
                    }
                return Response(response_data, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({'error': 'Access token has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.DecodeError:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Failed to retrieve access token'}, status=status.HTTP_400_BAD_REQUEST)





class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")

        if not access_token:
            return Response({"ok": False, "message": "Access Token required or expired"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = AccessToken(access_token)


            return Response({"ok": True, "message": "Logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
