from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import UserShortcut, ShortcutType
from account.utils import get_shortcut_url
from django.urls import reverse

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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
        
        return render(
            request,
            "auth_app/login.html",
            {"error_message": "メールアドレスまたはパスワードが違います。"}
        )

    return render(request, "auth_app/login.html")
    
    
def signup_view(request):
    if request.method == "POST":
        account_name = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        errors = {}

        if not account_name:
            errors["username"] = "アカウント名を入力してください。"

        if not email:
            errors["email"] = "メールアドレスを入力してください。"
        elif (
            User.objects.filter(email__iexact=email).exists()
            or User.objects.filter(username__iexact=email).exists()
        ):
            errors["email"] = "このメールアドレスはすでに使用されています。"

        if not password:
            errors["password"] = "パスワードを入力してください。"
        elif not password.isascii() or not password.isalnum():
            errors["password"] = "パスワードは半角英数字で入力してください。"
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                errors["password"] = e.messages[0]

        if not password_confirm:
            errors["password_confirm"] = "パスワード再入力を入力してください。"
        elif password != password_confirm:
            errors["password_confirm"] = "パスワードが一致しません。"

        if errors:
            return render(
                request,
                "auth_app/signup.html",
                {
                    "errors": errors,
                }
            )

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=account_name
            )
        except IntegrityError:
            return render(
                request,
                "auth_app/signup.html",
                {
                    "errors": {
                        "email": "登録に失敗しました。入力内容を確認してください。"
                    }
                }
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return render(
                request,
                "auth_app/signup.html",
                {
                    "errors": {
                        "email": "登録は完了しましたが、自動ログインに失敗しました。ログイン画面からログインしてください。"
                    }
                }
            )

        login(request, user)
        return redirect("auth_app:home")

    return render(request, "auth_app/signup.html")

@login_required
def home_view(request):
    print(request.user, request.user.is_authenticated)
    
    shortcuts = (
        UserShortcut.objects
        .filter(user=request.user)
        .select_related("shortcut_type")
        .order_by("position")
    )
    
    left_shortcut = None
    right_shortcut = None

    for shortcut in shortcuts:
        data = {
            "name": shortcut.shortcut_type.display_name,
            "url": get_shortcut_url(shortcut),
        }

        if shortcut.position == 1:
            left_shortcut = data
        elif shortcut.position == 2:
            right_shortcut = data
    
    #デフォルト：左側にメモ機能画面
    if not left_shortcut:
        left_shortcut = {
            "name": "メモ",
            "url": reverse("memos:memo_list"),
        }

        default_type = ShortcutType.objects.filter(action_key="memo").first()
        if default_type:
            UserShortcut.objects.update_or_create(
                user=request.user,
                position=1,
                defaults={"shortcut_type": default_type},
            )
    
    return render(
        request,
        "auth_app/home.html",
        {
            "left_shortcut": left_shortcut,
            "right_shortcut": right_shortcut,
        }
    )
