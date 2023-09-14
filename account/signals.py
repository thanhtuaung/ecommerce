from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from store.models import Customer

@receiver(post_save, sender=User)
def create_customer(sender, **kwargs):
    Customer.objects.create(
        user = sender,
        name = sender.username,
        email = sender.email
    )