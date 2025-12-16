from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .forms import AccountEditForm

# Create your views here.
def account(request):
    return render(request, 'account/account.html')

def logout(request):
    return render(request, 'account/logout.html')



#アカウント更新画面　モーダル表示
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
    
#パスワード編集画面　パスワード編集チェック
@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        
        #現在のパスワードチェック
        if not request.user.check_password(old_password):
            return render(request, "account/change_password.html",{
                "error" : "現在のパスワードがちがいます。"
            })
         
        #新しいパスワードの強度チェック
        try:
            validate_password(new_password, request.user)
        except ValidationError as e:
            return render(request, "account/change_password.html",{
                "error" : e.messages
            })        
            
        #パスワード更新    
        request.user.set_password(new_password)
        request.user.save()
        
        return redirect("password_complete")
    
    return render(request, "account/change_password.html")
            
            