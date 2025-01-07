from django.forms import ValidationError
from rest_framework import status, generics # type: ignore
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
from .decorators import GroupPermission
from django.contrib.auth.models import User, Group
from .custom_responses import CustomResponseMixin


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
        

class UserListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.add_user']


class UserUpdateDeleteRetriveView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_user', 'auth.change_user', 'auth.delete_user']


class GroupListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Group.objects.order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated,GroupPermission]
    required_permissions = ['auth.view_group', 'auth.add_group']


class GroupRetriveUpdateDeleteView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_group', 'auth.change_group', 'auth.delete_group']


class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.order_by('-id')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['auth.view_permission']



class SizeListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Size.objects.order_by('-id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_size', 'view_size']
    


class SizeRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.order_by('-id')
    serializer_class = SizeSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_size', 'view_size', 'delete_size']



class IngridientListCreateView(CustomResponseMixin, generics.ListCreateAPIView):
    queryset = Ingridients.objects.order_by('-id')
    serializer_class =  IngridientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['add_ingridient', 'view_ingridient']
    


class IngridientRetrieveUpdateDestroyView(CustomResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingridients.objects.order_by('-id')
    serializer_class = IngridientSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['change_ingridient', 'view_ingridient', 'delete_ingridient']


class IngridientInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = IngridientInvoice.objects.order_by('-id')
    serializer_class = IngridientInvoiceSerializer
    permission_classes = [IsAuthenticated]
    required_permissions = ['add_ingridientinvoiceitem', 'view_ingridientinvoiceitem']

    def create(self, request, *args, **kwargs):
        items_data = request.data.pop('items', None)
        if not items_data:
            raise ValidationError({"items": "This field is required and must contain valid data."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()

        for item in items_data:
            item['igridient_invoice'] = invoice.id
            item_serializer = IngridientInvoiceItemSerializer(data=item)
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()

        return Response(serializer.data, status=201)
    

class IngridientInvoiceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngridientInvoice.objects.order_by('-id')
    serializer_class = IngridientInvoiceSerializer
    permission_classes = [IsAuthenticated]
    required_permissions = ['add_ingridientinvoice', 'view_ingridientinvoice']

    def update(self, request, *args, **kwargs):
        items_data = request.data.get('items', None)
        status = request.data.get('status')

        instance = self.get_object()
        if instance.status != 'draft':
            raise ValidationError({"status": "Only invoices with 'draft' status can be updated."})

        if status not in ['accepted', 'canceled', 'draft']:
            raise ValidationError({"status": "Invalid status. Allowed values are 'draft', 'accepted', or 'canceled'."})

        if status == 'accepted' and not items_data:
            raise ValidationError({"items": "This field is required when status is 'accepted'."})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()


        if items_data and status == 'accepted':
            for item in items_data:
                item['igridient_invoice'] = invoice.id
                
                existing_item = IngridientInvoiceItem.objects.filter(igridient_invoice=invoice.id, ingridient=item['ingridient']).first()
                    # Create stock movement record
                if existing_item:
                    existing_item.quantity += item['quantity']
                    existing_item.price = item['price']
                    existing_item.save()
                else:
                    item_serializer = IngridientInvoiceItemSerializer(data=item)
                    item_serializer.is_valid(raise_exception=True)
                    item_serializer.save()

                stock_instance = Stock.objects.filter(ingridient=item['ingridient'], user=request.user).first()

                if stock_instance:
                    stock_instance.quantity += item['quantity']  
                    stock_instance.price = item['price']  
                    stock_instance.save()

                    stock_movement_data_update = {
                        'ingridient': item['ingridient'],  
                        'type': 'arrival',
                        'quantity': item['quantity'],
                        'user': request.user.id,
                        'description': 'Stock Updated'
                    }
                    stock_movement_serializer = StockMovementSerializer(data=stock_movement_data_update, context={'request': request})
                    stock_movement_serializer.is_valid(raise_exception=True)
                    stock_movement_serializer.save()

                else:
                    stock_data = {
                        'ingridient': item['ingridient'],
                        'quantity': item['quantity'],
                        'price': item['price'],
                        'user': request.user.id,  
                    }
                    stock_serializer = StockSerializer(data=stock_data, context={'request': request})
                    stock_serializer.is_valid(raise_exception=True)
                    stock_serializer.save()

                    stock_movement_data_new = {
                        'ingridient': item['ingridient'], 
                        'type': 'arrival',
                        'user': request.user.id,
                        'description': 'Stock Added'
                    }
                    stock_movement_serializer = StockMovementSerializer(data=stock_movement_data_new, context={'request': request})
                    stock_movement_serializer.is_valid(raise_exception=True)
                    stock_movement_serializer.save()

            return Response(serializer.data)



class IngridientInvoiceItemListView(CustomResponseMixin, generics.ListAPIView):
    queryset = IngridientInvoiceItem.objects.order_by('-id')
    serializer_class = IngridientInvoiceItemSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_ingridientinvoiceitem']



class StockListView(CustomResponseMixin, generics.ListAPIView):
    queryset = Stock.objects.order_by('-id')
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_stock']


class StockMovementListView(CustomResponseMixin, generics.ListAPIView):
    queryset = StockMovement.objects.order_by('-id')
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated, GroupPermission]
    required_permissions = ['view_stockmovement']