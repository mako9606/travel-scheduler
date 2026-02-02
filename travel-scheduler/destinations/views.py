from django.shortcuts import render
from django.shortcuts import render, redirect

# destination_search.html  
def destination_search(request):
    q = request.GET.get("q", "")

    # 仮の検索結果（model実装に変更する）
    destinations = []

    return render(
        request,
        "destinations/destination_search.html",
        {
            "q": q,
            "destinations": destinations,
        }
    )
    
# destination_edit.html  
# 今は保存処理なし（後で書く）
def destination_edit(request):
    if request.method == "POST":
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return render(request, "destinations/destination_edit.html")



# destination_delete.html  
def destination_delete(request):
    if request.method == 'POST':
        # 今は削除処理なし（model未実装のため）
        # 削除した体で plan_detail に戻す
        return redirect('plans:plan_detail')

    # GET のときは削除確認画面を表示
    return render(
        request,
        'destinations/destination_delete.html'
    )
    

# destination_detail.html
def destination_detail(request):
    # 今はダミーデータ（表示確認用）
    destination = {
        "open_time": "10:00",
        "close_time": "18:00",
        "closed_days": "水曜日",
        "parking": "あり",
        "price": "500",
    }

    return render(
        request,
        "destinations/destination_detail.html",
        {
            "destination": destination
        }
    )


#  map_destination.html
def map_destination(request):
    q = request.POST.get("q", "") if request.method == "POST" else ""

    context = {
        "q": q,
    }
    return render(request, "destinations/map_destination.html", context)


def map_pin_edit(request):
    return render(request, "destinations/map_pin_edit.html")


def map_pin_delete(request):
    return render(request, "destinations/map_pin_delete.html")