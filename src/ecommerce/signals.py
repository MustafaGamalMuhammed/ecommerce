from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ecommerce.models import Cart


def create_cart(sender, instance, **kwargs):
    Cart.objects.get_or_create(user=instance)


post_save.connect(create_cart, sender=User)