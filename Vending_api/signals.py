from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Sale

@receiver(post_save, sender=Sale)
def update_vending_machine_revenue(sender, instance, **kwargs):
    vending_machine = instance.vending_machine
    vending_machine.update_total_revenue()
