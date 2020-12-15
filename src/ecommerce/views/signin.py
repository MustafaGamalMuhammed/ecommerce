from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import django.contrib.auth as auth
from django.contrib import messages


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(
                    request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Wrong username or password')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])

    context = {
        'form': AuthenticationForm(),
    }

    return render(request, 'ecommerce/signin.html', context=context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')
