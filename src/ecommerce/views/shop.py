from django.shortcuts import render, get_object_or_404
from ecommerce.models import Subcategory


def shop(request, subcategory:str=None):
    if subcategory:
        subcategory = get_object_or_404(Subcategory, name=subcategory)

    context = {
        'subcategory': subcategory,
    }

    return render(request, 'ecommerce/shop.html', context=context)