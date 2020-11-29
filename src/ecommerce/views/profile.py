from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Profile, Category, Product
from .product import get_product_data


def get_profile_data(request, profile):
    data = {}
    data['user_profile'] = (request.user.profile == profile)
    data['username'] = profile.user.username
    data['products'] = []

    for product in profile.products.all():
        d = get_product_data(request, product)
        d['delete'] = False
        data['products'].append(d)

    return data


def profile(request, id):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'ecommerce/profile.html', context=context)

    
@api_view(['GET'])
def get_profile(request, id):
    try:
        profile = get_object_or_404(Profile, id=id)
        data = get_profile_data(request, profile)
        return Response(data=data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def update_profile(request):
    try:
        for p in request.data['products']:
            product = Product.objects.get(id=int(p['id']))
            
            if p.get('delete', False):
                product.delete()
            else:
                product.available = int(p['available'])
                product.save()

        data = get_profile_data(request, request.user.profile)        
        return Response(data=data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
