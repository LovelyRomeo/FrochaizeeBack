from django.contrib import admin
from .models import VendingMachines, Product, Sale, User, Maintenance

@admin.register(VendingMachines)
class VendingMachinesAdmin(admin.ModelAdmin):
    list_display = ('vendingID', 'vending_name', 'vending_model', 'address', 'vending_type', 'vending_status', 'payout_amount', 'vending_modem')
    search_fields = ('vending_model', 'address')
    list_filter = ('vending_status', 'vending_type')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productID', 'name', 'price', 'quantity_in_stock', 'min_stock')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'sale_date', 'payment_method']   
    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'full_name', 'email', 'phone', 'role')
    search_fields = ('full_name', 'email')

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('maintenanceID', 'vending_machine', 'maintenance_date', 'executor')
    search_fields = ('vending_machine__vendingID',)
    list_filter = ('maintenance_date',)