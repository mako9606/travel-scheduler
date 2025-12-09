from django.shortcuts import render

# Create your views here.
def account(request):
    return render(request, 'account/account.html')

def edit_email(request):
    return render(request, 'account/edit_email.html')

def change_password(request):
    return render(request, 'account/change_password.html')

def logout(request):
    return render(request, 'account/logout.html')
