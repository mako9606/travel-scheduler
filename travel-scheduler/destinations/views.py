from django.shortcuts import render, redirect, get_object_or_404
from plans.models import DaySchedule
from .models import Destination, MapPin
from .forms import DestinationForm, MapPinForm
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
    
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    
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
        form = DestinationForm(initial={
            "latitude": lat,
            "longitude": lng,
        })

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
    
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    
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
        if lat and lng:
            form = DestinationForm(
                instance=destination,
                initial={
                    "latitude": lat,
                    "longitude": lng,
                }
            )
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
        is_registered = day.schedules.filter(destination=destination).exists()
        
    return render(request, "destinations/destination_detail.html", {
        "destination": destination,
        "day": day,
        "is_registered": is_registered,
    })


#  map_destination.html
def map_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    pins = destination.pins.all().order_by("order")
    
    selected_pin_id = request.GET.get("pin_id")
    selected_pin = None

    if selected_pin_id:
        selected_pin = get_object_or_404(
            MapPin,
            pk=selected_pin_id,
            destination=destination
        )

    context = {
        "destination": destination,
        "pins": pins,
        "selected_pin": selected_pin,
    }

    return render(request, "destinations/map_destination.html", context)


#def map_pin_create(request, destination_id):
    #destination = get_object_or_404(Destination, pk=destination_id)

    #if request.method == "POST":
        #form = MapPinForm(request.POST)
        #if form.is_valid():
            #pin = form.save(commit=False)
            #pin.destination = destination
            #pin.save()
            #return redirect("destinations:map_destination", pk=destination.id)
    #else:
        #form = MapPinForm()

    #return render(request, "destinations/map_pin_edit.html", {
        #"form": form,
        #"destination": destination,
    #})

def map_pin_edit(request, destination_id):
    
    destination = get_object_or_404(Destination, pk=destination_id)
    pins = destination.pins.all().order_by("order")
    
     # GETパラメータから選択ピン取得
    selected_pin = None
    pin_id = request.GET.get("pin_id")
    
    print("destination_id:", destination_id)
    print("pin_id:", pin_id)
    print("method:", request.method)

    if pin_id:
        selected_pin = get_object_or_404(
            MapPin,
            pk=pin_id,
            destination=destination
        )

    # 追加処理（pin_idなし）
    if request.method == "POST" and request.POST.get("action") == "add":
        form = MapPinForm(request.POST)
        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.destination = destination
            new_pin.save()
            return redirect("destinations:map_destination", pk=destination.id)

    # 編集処理（pin_idあり）
    if request.method == "POST" and selected_pin:
        selected_pin.name = request.POST.get("name")
        selected_pin.save()
        return redirect(
            f"/destinations/map/{destination.id}/pin/edit/?pin_id={selected_pin.id}"
        )

    form = MapPinForm()

    return render(
        request,
        "destinations/map_pin_edit.html",
        {
            "destination": destination,
            "pins": pins,
            "form": form,
            "selected_pin": selected_pin,
        }
    )


def map_pin_delete(request, destination_id, pin_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    pin = get_object_or_404(MapPin, pk=pin_id, destination=destination)

    if request.method == "POST":
        pin.delete()
        return redirect("destinations:map_destination", pk=destination.id)

    return render(
        request,
        "destinations/map_pin_delete.html",
        {
            "destination": destination,
            "pin": pin,
        }
    )