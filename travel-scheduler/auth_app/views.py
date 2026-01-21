from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup_view(request):
    return render(request, 'auth_app/signup.html')

@login_required
def home_view(request):
    return render(request, 'auth_app/home.html')
