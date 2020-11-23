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
    page = request.GET.dict().pop('page')
    paginator = Paginator(get_products_data(request), 9)

    if page:
        products_page = paginator.get_page(page)
    else:
        products_page = paginator.get_page(1)

    page_data['page'] = page
    page_data['products'] = products_page.object_list

    return page_data


@api_view(['GET'])
def products(request:HttpRequest):
    return Response(data=get_page_data(request), status=status.HTTP_200_OK)