from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, VendingMachinesViewSet, SaleViewSet, UserViewSet, MaintenanceViewSet

router = DefaultRouter()
router.register(r'vending-machines', VendingMachinesViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'users', UserViewSet)
router.register(r'maintenance', MaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]