from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AccountEditFrom

# Create your views here.
def account(request):
    return render(request, 'account/account.html')

def edit_email(request):
    return render(request, 'account/edit_email.html')

def change_password(request):
    return render(request, 'account/change_password.html')

def logout(request):
    return render(request, 'account/logout.html')


@login_required
def edit_email(request):
    user = request.user
    
    if request.method == "POST":
        form = AccountEditFrom(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "アカウント名　メールアドレスを更新しました。")
            return redirect("account")
    
    else:
        form = AccountEditFrom(instance=user)
        
    return render(request, "account/edit_email.html",{
        "form" : form
    })    
    