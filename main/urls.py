from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    #AUTH APIS
    path('api-auth/login/', LoginView.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='logout'),
    #USER APIS
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/user/<int:pk>/', UserUpdateDeleteRetriveView.as_view(), name='user-update-delete-retrive'),
    #GROUP(ROLES) APIS
    path('api/roles/', GroupListCreateView.as_view(), name='roles-list-create'),
    path('api/role/<int:pk>/', GroupRetriveUpdateDeleteView.as_view(), name='role-update-delete-retrive'),
    #PERMISSION APIS
    path('api/permissions/', PermissionListView.as_view(), name='permissions-list')

]