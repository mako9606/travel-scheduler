from django.shortcuts import render, redirect, get_object_or_404
from plans.models import DaySchedule
from .models import Destination

# destination_search.html  
def destination_search(request):
    day_schedule_id = request.GET.get("day_schedule_id")
    day = None

    if day_schedule_id:
        day = get_object_or_404(DaySchedule, pk=day_schedule_id)

    q = request.GET.get("q", "")
    destinations = Destination.objects.filter(name__icontains=q) if q else []

    return render(request, "destinations/destination_search.html", {
        "day": day,
        "q": q,
        "destinations": destinations,
    })
    
    
    
# destination_edit.html  
# 今は保存処理なし（後で書く）
def destination_edit(request):
    if request.method == "POST":
        day_id = request.POST.get("day_schedule_id")
        if day_id:
            # 予定設定画面に遷移
            return redirect("plans:schedule_edit",day_schedule_id=day_id)

        # day がなければ検索画面に遷移
        return redirect("destinations:destination_search")
    return render(request, "destinations/destination_edit.html")


# destination_delete.html  
def destination_delete(request):
    if request.method == "POST":
        day_id = request.POST.get("day_schedule_id")

        if day_id:
            day = get_object_or_404(DaySchedule, pk=day_id)
            plan = day.plan 
            # 削除ボタン後 plan_detail（day付き）に遷移
            return redirect('plans:plan_detail', pk=plan.id)

    # GET：削除確認画面
    return render(request, 'destinations/destination_delete.html')
    

# destination_detail.html
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)

    day = None
    day_schedule_id = request.GET.get("day_schedule_id")

    if day_schedule_id:
        day = get_object_or_404(DaySchedule, pk=day_schedule_id)


    return render(request, "destinations/destination_detail.html", {
        "destination": destination,
        "day": day,
    })


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