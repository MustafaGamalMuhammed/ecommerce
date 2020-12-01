from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Profile, Product, Category


def get_likes_data(request):
    data = {}
    data['products_count'] = request.user.profile.likes.count()
    data['products'] = []

    for product in request.user.profile.likes.all():
        d = product.get_data(request)
        data['products'].append(d)

    return data


@login_required
def likes(request):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/likes.html', context=context)


@login_required
@api_view(['POST'])
def like(request, id):
    try:
        product = get_object_or_404(Product, id=id)
        request.user.profile.likes.add(product)
        data = get_likes_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET'])
def get_likes(request):
    data = get_likes_data(request)
    
    return Response(data=data, status=status.HTTP_200_OK)
    