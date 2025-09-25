from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request) :
    return render(request, 'Authentication/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('Authentication:login')
    else:
        form = SignUpForm()
    return render(request, 'Authentication/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('emissions:company_dashboard', company_id=user.profile.company.id)  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'Authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('Authentication:home')


