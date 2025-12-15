from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AccountEditForm

# Create your views here.
def account(request):
    return render(request, 'account/account.html')

def edit_email(request):
    return render(request, 'account/edit_email.html')

def change_password(request):
    return render(request, 'account/change_password.html')

def logout(request):
    return render(request, 'account/logout.html')


#モーダル表示
@login_required
def edit_email(request):
    user = request.user
    
    if request.method == "POST":
        form = AccountEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, "account/edit_email.html",{
                "form" : form,
                "show_modal" : True,
            })
    
    else:
        form = AccountEditForm(instance=user)
        
    return render(request, "account/edit_email.html",{
        "form" : form
    })    
    