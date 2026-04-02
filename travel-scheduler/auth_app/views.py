from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import UserShortcut, ShortcutType
from account.utils import get_shortcut_url
from django.urls import reverse

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
            "url": get_shortcut_url(shortcut.shortcut_type.action_key),
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
