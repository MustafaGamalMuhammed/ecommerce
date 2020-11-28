from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ecommerce.models import Profile, Cart


def create_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    if created:
        cart = Cart()
        cart.save()
        profile.cart = cart
        profile.save()

post_save.connect(create_profile, sender=User)