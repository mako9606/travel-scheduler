from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash

from .forms import AccountEditForm

from account.models import UserShortcut, ShortcutType


@login_required
def account(request):

    if request.method == "POST":
        left_id = request.POST.get("left_shortcut")
        right_id = request.POST.get("right_shortcut")

        if left_id:
            UserShortcut.objects.update_or_create(
                user=request.user,
                position=1,
                defaults={"shortcut_type_id": left_id},
            )

        if right_id:
            UserShortcut.objects.update_or_create(
                user=request.user,
                position=2,
                defaults={"shortcut_type_id": right_id},
            )
        else:
            UserShortcut.objects.filter(
                user=request.user,
                position=2
            ).delete()    

        return redirect("account:account")

    shortcut_types = ShortcutType.objects.all()

    shortcuts = UserShortcut.objects.filter(user=request.user)

    left_selected = shortcuts.filter(position=1).first()
    right_selected = shortcuts.filter(position=2).first()

    return render(
        request,
        "account/account.html",
        {
            "shortcut_types": shortcut_types,
            "left_selected": left_selected.shortcut_type_id if left_selected else None,
            "right_selected": right_selected.shortcut_type_id if right_selected else None,
            "user_obj": request.user,
        },
    )


#　edit_email.html
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
        old_password = request.POST.get("old_password", "")
        new_password = request.POST.get("new_password", "")
        
        old_password_error = None
        new_password_errors = []
        
        #現在のパスワードチェック
        if not old_password_error:
            try:
                validate_password(new_password, request.user)
            except ValidationError as e:
                new_password_errors = e.messages

        if old_password_error or new_password_errors:
            return render(request, "account/change_password.html", {
                "old_password_error": old_password_error,
                "new_password_errors": new_password_errors,
            })        
            
        #パスワード更新    
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, "account/change_password.html", {
            "show_modal": True,
        })
    
    return render(request, "account/change_password.html")


#パスワード再設定完了画面
@login_required
def password_complete(request):
    return render(request, 'account/password_complete.html')


#ログアウト画面
@login_required            
def logout(request):
    return render(request, 'account/logout.html')            