from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
# Create your models here.
class VendingMachines(models.Model):                                                                
    vendingID = models.CharField(
        max_length=355,
        verbose_name='ID аппарата',
        )
    
    address = models.CharField(
        max_length=355,
        verbose_name='Адрес или описание места установки устройства'
        )
    
    vending_name = models.CharField(
        max_length=100,
        verbose_name="Название аппарата"
    )
    
    vending_modem = models.CharField(
        max_length=55,
        verbose_name='Модем',
        )
    
    vending_model = models.CharField(
        max_length=355, 
        verbose_name='Указание на марку и модель вендингового аппарата'
        )
    
    PAYMENT_CHOICES = [                                                                            
        ('card', 'С оплатой картой'),
        ('cash', 'С оплатой наличными'),
        ('card-cash', 'Два вида оплаты'),
        ]
    
    vending_type = models.CharField(
        max_length=10,  
        choices=PAYMENT_CHOICES,
        default='card',                                                                            
        verbose_name='Тип аппарата по способу оплаты'
        )
    
    STATUS_CHOICES = [                                                                              
        ('working', 'Рабочий'),
        ('not_working', 'Не рабочий'),
        ('in_service', 'На обслуживании'),
        ]
    
    vending_status = models.CharField(
        max_length=20,  
        choices=STATUS_CHOICES,
        default='working',                                                                          
        verbose_name='Статус аппарата'
        )
    
    date_of_installation = models.DateField(                                                        
        verbose_name='Дата установки'
        )
    
    date_of_last_maintenance = models.DateField(
        verbose_name='Дата последнего обслуживания'
        )
    
    payout_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0,
        verbose_name='Общая сумма продаж'
        )
    
    def update_total_revenue(self):
        total_income = Decimal('0.0') 
        for sale in self.sales.all():
            total_income += sale.product.price * Decimal(sale.quantity)  
        self.payout_amount = total_income
        self.save()
        
    class Meta:
        verbose_name = 'Вендинговый аппарат'
        verbose_name_plural = 'Вендинговые аппараты'

    def __str__(self):
        return f"{self.vendingID} ({self.address})"


class Product(models.Model):
    productID = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name='Уникальный идентификатор товара'
        )
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название товара'
        )
    
    description = models.TextField(
        verbose_name='Описание товара'
        )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Цена'
        )
    
    quantity_in_stock = models.PositiveIntegerField(
        verbose_name='Количество в наличии'
        )
    
    min_stock = models.PositiveIntegerField(
        verbose_name='Минимальный запас'
        )
    
    sales_trends = models.FloatField(
        verbose_name='Склонности к продажам'
        )

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
     
    def __str__(self):
        return str(self.productID)
    
    
class Sale(models.Model):
    sale_id = models.AutoField(
        primary_key=True,
        verbose_name='Уникальный идентификатор записи о продаже'
        )
    
    vending_machine = models.ForeignKey(
        VendingMachines,
        related_name='sales',   
        on_delete=models.CASCADE,
        verbose_name='Вендинговый аппарат'
        )
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name='ID товара'
        )
    
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
        )
    
    sale_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата и время продажи'
        )

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('QR', 'QR'),
    ]
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='card', verbose_name='Метод оплаты')

    sale_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма продажи',
        null=True,  
        blank=True
    )

    def save(self, *args, **kwargs):
        self.sale_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)



    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return f"Sale of {self.product.productID} x {self.quantity} on {self.sale_date}"
    
@receiver(post_save, sender=Sale)
def update_vending_machine_revenue(sender, instance, **kwargs):
    vending_machine = instance.vending_machine
    vending_machine.update_total_revenue()
    
class User(models.Model):
    userID = models.PositiveIntegerField(
        primary_key=True,
        verbose_name='Уникальный идентификатор пользователя'
        )
    
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО пользователя'
        )
    
    email = models.EmailField(
        max_length=255,
        verbose_name='Email'
        )
    
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон'
        )
    
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('operator', 'Оператор'),
        ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name='Роль'
        )
    
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
     

    def __str__(self):
        return self.full_name
    
    
class Maintenance(models.Model):
    maintenanceID = models.PositiveIntegerField(
        primary_key=True, 
        verbose_name='Уникальный идентификатор записи о обслуживании'
        )
    
    vending_machine = models.ForeignKey(
        VendingMachines,
        on_delete=models.CASCADE,
        verbose_name='ID аппарата'
        )
    
    maintenance_date = models.DateField(
        verbose_name='Дата обслуживания'
        )
    
    work_description = models.TextField(
        verbose_name='Описание работы'
        )
    problems_identified = models.TextField(
        blank=True,
        verbose_name='Проблемы'
        )
    
    executor = models.CharField(
        max_length=255, 
        verbose_name='Исполнитель'
        )

    class Meta:
        verbose_name = 'Обслуживание'
        verbose_name_plural = 'Обслуживание'
     
    
    def __str__(self):
        return f"Обслуживание {self.maintenanceID} - {self.vending_machine.vending_model} на {self.maintenance_date}"
    

