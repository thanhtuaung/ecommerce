from django.shortcuts import render, redirect
from django.http import HttpRequest

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from store.models import Customer
from django.contrib import messages

def login_view(request : HttpRequest):
    # if request.user.is_authenticated:
    #     return redirect('store')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, message='Invalide emaill or password')
            return redirect('login')

    return render(request, 'account/login.html')

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('login')


def register_view(request):

    form = RegisterForm()

    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)
    
        if form.is_valid():
            user = form.save()

            if user is not None:
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email
                )

                login(request, user)
                return redirect('store')
        
    context = {'form': form}
    return render(request, 'account/register.html', context)

