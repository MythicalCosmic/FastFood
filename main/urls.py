from django.urls import path # type: ignore
from .views import *

urlpatterns = [
    path('api-auth/login/', LoginView.as_view(), name='login'),
    path('api-auth/logout/', LogoutView.as_view(), name='logout'),
]