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
    path('api/permissions/', PermissionListView.as_view(), name='permissions-list'),
    #SIZE APIS
    path('api/sizes/', SizeListCreateView.as_view(), name='size-list-create'),
    path('api/size/<int:pk>/', SizeRetrieveUpdateDestroyView.as_view(), name='size-update-delete-retrive'),
    #INGRIDIENT APIS
    path('api/ingridients/', IngridientListCreateView.as_view(), name='ingridient-list-create'),
    path('api/ingridient/<int:pk>/', IngridientRetrieveUpdateDestroyView.as_view(), name='ingridient-update-destroy-retrive'),
    #INGRIDIENTINVOICE APIS
    path('api/ingridient-invoices/', IngridientInvoiceListCreateView.as_view(), name='ingridient-list-create'),
    path('api/ingridient-invoice/<int:pk>/', IngridientInvoiceRetrieveUpdateDeleteView.as_view(), name='ingridient-update-destroy-retrive'),
    #INGRIDIENTINVOICE ITEM APIS
    path('api/ingridient-invoice-items/', IngridientInvoiceItemListView.as_view(), name='ingridient-item-list'),
    #STOCK APIS
    path('api/stocks/', StockListView.as_view(), name='stock-list'),
    #STOCK MOVEMENT APIS
    path('api/stock-movement/', StockMovementListView.as_view(), name="stock-movement-list")
]