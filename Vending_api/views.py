from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, VendingMachines, Sale, Maintenance, User
from .serializers import ProductSerializer, VendingMachinesSerializer, SaleSerializer, MaintenanceSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import csv
from django.http import HttpResponse

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class VendingMachinesViewSet(viewsets.ModelViewSet):
    queryset = VendingMachines.objects.all()
    serializer_class = VendingMachinesSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    
class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
@api_view(['GET'])
def ExportVendingMachines(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="vending.csv"' 

    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([
        "ID", "Адресс", "Название автомата", 
        "Модем", "Модель", "Тип автомата", 
        "Статус", "Дата установки", 
        "Дата последнего обслуживания", "Общий заработок"
    ])

    for vending_machine in VendingMachines.objects.all().values_list(
        'vendingID', 'address', 'vending_name', 
        'vending_modem', 'vending_model', 'vending_type', 
        'vending_status', 'date_of_installation', 
        'date_of_last_maintenance', 'payout_amount'
    ):
        row = list(vending_machine)   
        writer.writerow(row)

    return response