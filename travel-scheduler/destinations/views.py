from django.shortcuts import render, redirect, get_object_or_404
from plans.models import DaySchedule
from .models import Destination
from .forms import DestinationForm
from django.urls import reverse
from django.http import HttpResponseRedirect

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


# destination_edit.html 新規作成時
def destination_create(request):
    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    day = get_object_or_404(DaySchedule, pk=day_schedule_id) if day_schedule_id else None

    if request.method == "POST":
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user
            destination.save()
        return redirect(
            f"{reverse('destinations:destination_search')}?day_schedule_id={day.id}"
        )
    
    else:
        form = DestinationForm()

    return render(
        request,
        "destinations/destination_edit.html",
        {
            "form": form,
            "destination": None,
            "day": day,
        }
    ) 
    
# destination_edit.html  
def destination_edit(request, pk):    
    destination = get_object_or_404(Destination, pk=pk)
    
    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    day = get_object_or_404(DaySchedule, pk=day_schedule_id) if day_schedule_id else None

    if request.method == "POST":
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user
            destination.save()
        
        if day:
            # プラン内
            return redirect(
                reverse("plans:schedule_create")
                + f"?day_schedule_id={day.id}&destination_id={destination.id}"
            )

        # プラン外　→　検索画面に遷移
        return redirect("destinations:destination_search")
    
    else:
        form = DestinationForm(instance=destination)

    return render(
        request,
        "destinations/destination_edit.html",
        {
            "form": form,
            "destination": destination,
            "day": day,
        }
    )


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
    is_registered = False

    day_schedule_id = request.GET.get("day_schedule_id")
    if day_schedule_id:
        day = get_object_or_404(DaySchedule, pk=day_schedule_id)
        is_registered = day.schedules.filter(destinations=destination).exists()
        
    return render(request, "destinations/destination_detail.html", {
        "destination": destination,
        "day": day,
        "is_registered": is_registered,
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