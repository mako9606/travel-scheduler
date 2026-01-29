from django.shortcuts import render
from django.shortcuts import get_object_or_404
from plans.models import Plan, DaySchedule
from destinations.models import Schedule


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
from django.shortcuts import render, redirect

def destination_edit(request):
    if request.method == "POST":
        # 今は保存処理なし（後で書く）
        return redirect("plans:plan_detail")

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
    
    
#  schedule_edit.html
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    destination = schedule.destination
    day = schedule.day

    if request.method == "POST":
        schedule.arrival_time = request.POST.get("arrival_time")
        schedule.departure_time = request.POST.get("departure_time")
        schedule.memo = request.POST.get("memo")
        schedule.save()

        return redirect(
            "plans:plan_detail",
            plan_id=day.plan.id
        )

    return render(
        request,
        "destinations/schedule_edit.html",
        {
            "schedule": schedule,
            "destination": destination,
            "day": day,
        }
    )
    
#  schedule_memo.html
def schedule_memo(request):
    if request.method == "POST":
        # 今は保存しない
        return redirect("plans:plan_detail")

    return render(
        request,
        "destinations/schedule_memo.html",
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