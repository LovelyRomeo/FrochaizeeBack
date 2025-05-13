from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Register.views import ConfirmEmailView, RegisterView
from Vending_api.views import ExportVendingMachines

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Vending_api.urls')),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('export/', ExportVendingMachines, name='export_CVM')
]


