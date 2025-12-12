from django.shortcuts import render

# Create your views here.
def signup_view(request):
    return render(request, 'auth_app/signup.html')

def home_view(request):
    return render(request, 'auth_app/home.html')
