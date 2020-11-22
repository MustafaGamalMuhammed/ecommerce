from django.shortcuts import render, redirect
import django.contrib.auth as auth


def signin(request):
    return render(request, 'ecommerce/signin.html')


def logout(request):
    auth.logout(request)
    return redirect('home')