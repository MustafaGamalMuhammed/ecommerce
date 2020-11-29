import django
from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Category, ProductReview


def get_product_data(request, product):
    d = {}
    d['id'] = product.id
    d['name'] = product.name
    d['rating'] = product.rating
    d['price'] = product.price
    d['image'] = product.image.url
    d['available'] = product.available
    d['url'] = product.get_absolute_url()
    d['description'] = product.description
    d['is_authenticated'] = request.user.is_authenticated

    if request.user.is_authenticated:
        d['is_liked'] = product in request.user.profile.likes.all()
        d['is_in_cart'] = request.user.profile.cart.has_product(product)
    
    d['reviews'] = []

    for review in product.reviews.all():
        r = get_review_data(review)    
        d['reviews'].append(r)

    return d


def get_products_data(request:HttpRequest):
    params = request.GET.dict()
    
    if params.get('page'):
        params.pop('page')
    
    products = Product.objects.filter(**params)
    data = []

    for product in products:
        d = get_product_data(request, product)
        data.append(d)

    return data


def get_review_data(review):
    r = {}
    r['id'] = review.id
    r['username'] = review.user.username
    r['rating'] = review.rating
    r['content'] = review.content

    return r


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
        data = get_product_data(request, product)
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def post_review(request):
    try:
        user_id = int(request.data.get('user_id')) 
        product_id = int(request.data.get('product_id'))
        rating = int(request.data.get('rating'))
        content = request.data.get('content')

        review = ProductReview.objects.create(user_id=user_id, product_id=product_id, rating=rating, content=content)
        data = get_review_data(review)
        return Response(data=data, status=status.HTTP_200_OK)
    except (TypeError, django.core.exceptions.FieldError):
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        