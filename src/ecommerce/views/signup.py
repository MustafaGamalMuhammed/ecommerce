from django.shortcuts import render, redirect
from django.contrib import messages
from ecommerce.forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])

    context = {
        'form': SignupForm(),
    }

    return render(request, 'ecommerce/signup.html', context=context)
