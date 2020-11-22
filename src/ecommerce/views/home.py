from django.shortcuts import render
from ecommerce.models import Category


def home(request):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/home.html', context=context)