from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Category, CartItem


def get_cart_data(request):
    data = {}
    data['items_count'] = request.user.profile.cart.items.count()
    data['items'] = []

    for item in request.user.profile.cart.items.all():
        data['items'].append(item.get_data(request))

    return data


def update_cart_items(request):
    for item in request.data['items']:
        id, quantity = int(item['id']), int(item['quantity'])
        cart_item = CartItem.objects.get(id=id)

        if item.get('delete', False):
            cart_item.delete()
        else:
            cart_item.quantity = quantity 
            cart_item.save()


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
        product = Product.objects.get(id=id)
        request.user.profile.cart.items.create(product=product)
        data = get_cart_data(request)
        return Response(data=data, status=status.HTTP_201_CREATED)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def get_cart(request):
    try:
        data = get_cart_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def update_cart(request):
    try:
        update_cart_items(request)
        data = get_cart_data(request)
        return Response(data=data, status=status.HTTP_201_CREATED)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
