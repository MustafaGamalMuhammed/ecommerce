from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Category, CartItem
from .product import get_product_data


def get_cart_data(request):
    data = {}
    data['items_count'] = request.user.profile.cart.items.count()
    data['total_price'] = request.user.profile.cart.total_price
    data['items'] = []

    for item in request.user.profile.cart.items.all():
        d = {}
        d['id'] = item.id
        d['quantity'] = item.quantity
        d['delete'] = False
        d['product'] = get_product_data(request, item.product)
        d['total_price'] = item.total_price
        data['items'].append(d)

    return data


@login_required
def cart(request):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/cart.html', context=context)


@login_required
@api_view(['POST'])
def add_to_cart(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        request.user.profile.cart.items.create(product=product)
        data = get_cart_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def get_cart(request):
    data = get_cart_data(request)

    return Response(data=data, status=status.HTTP_200_OK)


@login_required
@api_view(['POST'])
def update_cart(request):
    try:    
        for item in request.data['items']:
            cart_item = CartItem.objects.get(id=int(item['id']))
            
            if item.get('delete', False):
                cart_item.delete()
            else:
                cart_item.quantity = int(item['quantity'])
                cart_item.save()

        data = get_cart_data(request)        
        return Response(data=data, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
