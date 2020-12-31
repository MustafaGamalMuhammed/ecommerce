from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Profile, Category, Product
from ecommerce.forms import ProductForm


def update_profile_products(request):
    for p in request.data['products']:
        product = Product.objects.get(id=int(p['id']))

        if p.get('delete', False):
            product.delete()
        else:
            product.available = int(p['available'])
            product.save()


def profile(request, id):
    context = {
        'categories': Category.objects.all(),
        'form': ProductForm(),
    }

    return render(request, 'ecommerce/profile.html', context=context)


@api_view(['GET'])
def get_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        data = profile.get_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def update_profile(request):
    try:
        update_profile_products(request)
        data = request.user.profile.get_data(request)
        return Response(data=data, status=status.HTTP_200_OK)
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
