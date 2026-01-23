from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        email = request.POST["username"]
        password = request.POST["password"]
        
        print("views側:", email)

        user = authenticate(request, username=email, password=password)
        print("authenticate結果:", user)

        if user is not None:
            login(request, user)
            return redirect("auth_app:home")
    return render(request, "auth_app/login.html")
    
    
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        user = authenticate(request,username=email, password=password)
        login(request, user)
        
        return redirect("auth_app:home")
    
    return render(request, 'auth_app/signup.html')

@login_required
def home_view(request):
    print(request.user, request.user.is_authenticated)
    return render(request, 'auth_app/home.html')
