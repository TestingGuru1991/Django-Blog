from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # The user wants to sign up
        if request.POST['username'] and request.POST['email'] and request.POST['password1'] and request.POST['password2']:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken.'})
                except User.DoesNotExist:
                    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                    password=request.POST['password1'])
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'accounts/signup.html', {'error': 'Passwords must match.'})
        else:
            return render(request, 'accounts/signup.html', {'error': 'All fields are required.'})
    else:
        # user wants to enter info
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
