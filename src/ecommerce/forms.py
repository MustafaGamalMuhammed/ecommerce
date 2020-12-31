from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from ecommerce.models import Product


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'subcategory', 'price', 'image', 'available', 'sold', 'description']
