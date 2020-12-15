import django
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Category, ProductReview
from ecommerce.forms import ProductForm


def get_products_data(request):
    params = request.GET.dict()

    if params.get('page'):
        params.pop('page')

    products = Product.objects.filter(**params)
    data = []

    for product in products:
        data.append(product.get_data(request))

    return data


def get_page_data(request):
    data = dict()
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(get_products_data(request), 9)
    page = paginator.get_page(page_num)

    data['page'] = page_num
    data['products'] = page.object_list
    data['has_previous'] = page.has_previous()
    data['has_next'] = page.has_next()

    return data


def get_review_data_from_request(request):
    data = {}
    data['user_id'] = int(request.data.get('user_id'))
    data['product_id'] = int(request.data.get('product_id'))
    data['rating'] = int(request.data.get('rating'))
    data['content'] = request.data.get('content')

    return data


def product(request, id):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/product.html', context=context)


@api_view(['GET'])
def products(request):
    try:
        data = get_page_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_product(request, id):
    try:
        product = Product.objects.get(id=id)
        data = product.get_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@require_POST
def post_product(request):
    try:
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = Product.objects.create(
                seller=request.user.profile,
                **form.cleaned_data)
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])

        return redirect(request.user.profile)
    except:
        return redirect(request.user.profile)


@login_required
@api_view(['POST'])
def post_review(request):
    try:
        review = ProductReview.objects.create(**get_review_data_from_request(request))
        data = review.get_data()
        return Response(data=data, status=status.HTTP_201_CREATED)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
