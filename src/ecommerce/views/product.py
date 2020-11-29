import django
from django.shortcuts import render, get_object_or_404, redirect
from django.http.request import HttpRequest
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Category, ProductReview
from ecommerce.forms import ProductForm


def get_products_data(request:HttpRequest):
    params = request.GET.dict()
    
    if params.get('page'):
        params.pop('page')
    
    products = Product.objects.filter(**params)
    data = []

    for product in products:
        data.append(product.get_data(request))

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


def product(request, id):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/product.html', context=context)


@api_view(['GET'])
def products(request:HttpRequest):
    try:
        data = get_page_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except django.core.exceptions.FieldError:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_product(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        data = product.get_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@require_POST
def post_product(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = Product.objects.create(seller_id=int(request.POST.get('seller_id')), **form.cleaned_data)
    
    return redirect(request.user.profile)    



@login_required
@api_view(['POST'])
def post_review(request):
    try:
        user_id = int(request.data.get('user_id')) 
        product_id = int(request.data.get('product_id'))
        rating = int(request.data.get('rating'))
        content = request.data.get('content')

        review = ProductReview.objects.create(user_id=user_id, product_id=product_id, rating=rating, content=content)
        data = review.get_data()
        return Response(data=data, status=status.HTTP_200_OK)
    except (TypeError, django.core.exceptions.FieldError):
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
