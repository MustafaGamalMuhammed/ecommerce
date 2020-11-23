from django.shortcuts import render, get_object_or_404
from ecommerce.models import Subcategory, Category


def shop(request):
    context = {
        'categories': Category.objects.all(),
    }

    if request.GET.get('subcategory'):
        subcategory = get_object_or_404(Subcategory, name=request.GET.get('subcategory'))
        context['subcategory'] = subcategory

    return render(request, 'ecommerce/shop.html', context=context)