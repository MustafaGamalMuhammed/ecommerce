from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@login_required
def cart(request):
    return render(request, 'ecommerce/cart.html')


def get_cart_data(request):
    data = {}
    data['products_count'] = request.user.profile.cart.products.count()

    return data


@login_required
@api_view(['GET'])
def get_cart(request):
    data = get_cart_data(request)

    return Response(data=data, status=status.HTTP_200_OK)