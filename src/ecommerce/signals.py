from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ecommerce.models import Profile, Cart


def create_profile(sender, instance, **kwargs):
    cart = Cart()
    cart.save()
    Profile.objects.get_or_create(user=instance, cart=cart)


post_save.connect(create_profile, sender=User)