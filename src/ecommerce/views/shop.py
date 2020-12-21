from django.shortcuts import render, get_object_or_404
from ecommerce.models import Subcategory, Category


def shop(request):
    context = {
        'categories': Category.objects.all(),
    }

    category_name = request.GET.get('subcategory__name')
    
    if category_name:
        subcategory = get_object_or_404(Subcategory, name=category_name)
        context['subcategory'] = subcategory

    return render(request, 'ecommerce/shop.html', context=context)
