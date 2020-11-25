from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Profile


@login_required
def likes(request):
    return render(request, 'ecommerce/likes.html')


def get_likes_data(request):
    data = {}
    data['products_count'] = request.user.profile.likes.count()

    return data


@login_required
@api_view(['GET'])
def get_likes(request):
    data = get_likes_data(request)
    
    return Response(data=data, status=status.HTTP_200_OK)