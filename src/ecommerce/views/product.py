import django
from django.shortcuts import render
from django.http.request import HttpRequest
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product


def product(request, id):
    return render(request, 'ecommerce/product.html')


def get_products_data(request:HttpRequest):
    params = request.GET.dict()
    
    if params.get('page'):
        params.pop('page')
    
    products = Product.objects.filter(**params)
    data = []

    for product in products:
        d = {}
        d['name'] = product.name
        d['price'] = product.price
        d['image'] = product.image.url
        d['url'] = product.get_absolute_url()
        data.append(d)

    return data


def get_page_data(request:HttpRequest):
    page_data = dict()
    page = int(request.GET.get('page', 1))
    paginator = Paginator(get_products_data(request), 9)

    products_page = paginator.get_page(page)

    page_data['page'] = page
    page_data['products'] = products_page.object_list
    page_data['has_previous'] = products_page.has_previous()
    page_data['has_next'] = products_page.has_next()

    return page_data


@api_view(['GET'])
def products(request:HttpRequest):
    try:
        data = get_page_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except django.core.exceptions.FieldError:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)