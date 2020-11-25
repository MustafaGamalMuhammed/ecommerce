from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product


@login_required
def cart(request):
    return render(request, 'ecommerce/cart.html')


def get_cart_data(request):
    data = {}
    data['products_count'] = request.user.profile.cart.products.count()

    return data


@login_required
@api_view(['POST'])
def add_to_cart(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        request.user.profile.cart.products.add(product)
        data = get_cart_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def get_cart(request):
    data = get_cart_data(request)

    return Response(data=data, status=status.HTTP_200_OK)