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

    destination_modal_id = request.GET.get("destination_modal_id")
    modal_destination = None
    if destination_modal_id:
        modal_destination = get_object_or_404(Destination, pk=destination_modal_id)

    if day:
        is_owner = request.user.is_authenticated and day.plan.user == request.user
        is_shared_viewer = request.session.get("shared_plan_id") == day.plan.id
    else:
        is_owner = request.user.is_authenticated
        is_shared_viewer = False

    return render(request, "destinations/destination_search.html", {
        "day": day,
        "q": q,
        "destinations": destinations,
        "modal_destination": modal_destination,
        "is_owner": is_owner,
        "is_shared_viewer": is_shared_viewer,
    })


# destination_edit.html 新規作成時
def destination_create(request):
    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    day = get_object_or_404(DaySchedule, pk=day_schedule_id) if day_schedule_id else None
    
    from_page = request.GET.get("from") or request.POST.get("from")
    schedule_id = request.GET.get("schedule_id") or request.POST.get("schedule_id")

    
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    
    if request.method == "POST":
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user

            closed_days = request.POST.getlist("closed_day")
            destination.closed_day = ",".join(closed_days)

            destination.save()
            
            action = request.POST.get("action")
            
            if action == "save_and_map":
                url = reverse("destinations:map_destination", kwargs={"pk": destination.id})

                params = []
                if day:
                    params.append(f"day_schedule_id={day.id}")
                if from_page:
                    params.append(f"from={from_page}")
                if schedule_id:
                    params.append(f"schedule_id={schedule_id}")

                if params:
                    url += "?" + "&".join(params)

                return redirect(url)

            if day:
                return redirect(
                    reverse("plans:schedule_create")
                    + f"?day_schedule_id={day.id}&destination_id={destination.id}"
                )

            return redirect("destinations:destination_search")
    
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
            "from_page": from_page,
            "schedule_id": schedule_id,
        }
    ) 
    
# destination_edit.html  
def destination_edit(request, pk):    
    destination = get_object_or_404(Destination, pk=pk)
    
    if destination.user != request.user:
        return redirect("plans:plan_list")
    
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    
    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    from_page = request.GET.get("from") or request.POST.get("from")
    day = get_object_or_404(DaySchedule, pk=day_schedule_id) if day_schedule_id else None
    schedule_id = request.POST.get("schedule_id") or request.GET.get("schedule_id")

    if request.method == "POST":
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.user = request.user

            closed_days = request.POST.getlist("closed_day")
            destination.closed_day = ",".join(closed_days)

            destination.save()
            
            action = request.POST.get("action")

            if day and action == "save_and_set":
                return redirect(
                    reverse("plans:schedule_create")
                    + f"?day_schedule_id={day.id}&destination_id={destination.id}"
                )

        
            if day:  # プラン内
                url = reverse("destinations:destination_detail", kwargs={"pk": destination.id}) + f"?day_schedule_id={day.id}"
                if from_page == "search":
                    url += "&from=search"
                if schedule_id:
                    url += f"&schedule_id={schedule_id}"
                return redirect(url)

            # プラン外　→　検索画面に遷移
            return redirect(
                reverse("destinations:destination_detail", kwargs={"pk": destination.id})
            )
    
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
            "from_page": from_page,
            "schedule_id": schedule_id,
        }
    )


# destination_delete.html  
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)

    if destination.user != request.user:
        return redirect("plans:plan_list")

    day_schedule_id = request.POST.get("day_schedule_id") or request.GET.get("day_schedule_id")
    from_page = request.POST.get("from") or request.GET.get("from")
    schedule_id = request.POST.get("schedule_id") or request.GET.get("schedule_id")

    day = get_object_or_404(DaySchedule, pk=day_schedule_id) if day_schedule_id else None
    
    if request.method == "POST":
        # ここは削除対象の仕様確認後に確定
        destination.delete()

        if day:
            return redirect(
                f"{reverse('plans:plan_detail', kwargs={'pk': day.plan.id})}?day_schedule_id={day.id}"
            )
        return redirect("destinations:destination_search")

    return render(
        request,
        "destinations/destination_delete.html",
        {
            "destination": destination,
            "day": day,
            "from_page": from_page,
            "schedule_id": schedule_id,
        }
    )
    

# destination_detail.html
def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)

    day = None
    day_schedule_id = request.GET.get("day_schedule_id")
    schedule_id = request.GET.get("schedule_id")
    map_tab = request.GET.get("map_tab")
    
    if day_schedule_id:
        day = get_object_or_404(DaySchedule, pk=day_schedule_id)
        
    from_page = request.GET.get("from")    

    is_owner = request.user.is_authenticated and destination.user == request.user
    is_shared_viewer = day and request.session.get("shared_plan_id") == day.plan.id

    if not is_owner and not is_shared_viewer:
        return redirect("plans:plan_list")
    
    if from_page == "search":
        url = reverse("destinations:destination_search") + f"?destination_modal_id={destination.id}"
        if day:
            url += f"&day_schedule_id={day.id}"
        return redirect(url)
    
    if day:
        url = (
            f"{reverse('plans:plan_detail', kwargs={'pk': day.plan.id})}"
            f"?day_schedule_id={day.id}&destination_modal_id={destination.id}"
        )
        if schedule_id:
            url += f"&schedule_id={schedule_id}"
        if map_tab:
            url += f"&map_tab={map_tab}"    
        return redirect(url)

    return redirect(
        f"{reverse('destinations:destination_search')}"
        f"?destination_modal_id={destination.id}"
    )

#  map_destination.html
def map_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk, user=request.user)
    pins = MapPin.objects.filter(user=request.user).order_by("order", "id")

    selected_pin_id = request.GET.get("pin_id") or request.POST.get("pin_id")
    selected_pin = None

    if selected_pin_id:
        selected_pin = get_object_or_404(
            MapPin,
            pk=selected_pin_id,
            user=request.user
        )
    elif destination.selected_pin and destination.selected_pin.user == request.user:
        selected_pin = destination.selected_pin

    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    from_page = request.GET.get("from") or request.POST.get("from")
    schedule_id = request.GET.get("schedule_id") or request.POST.get("schedule_id")

    if request.method == "POST":
        action = request.POST.get("action")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        q = request.POST.get("q", "")

        if action == "search":
            context = {
                "destination": destination,
                "pins": pins,
                "selected_pin": selected_pin,
                "day_schedule_id": day_schedule_id,
                "from_page": from_page,
                "schedule_id": schedule_id,
                "q": q,
            }
            return render(request, "destinations/map_destination.html", context)

        if action == "save":
            if lat and lng:
                destination.latitude = lat
                destination.longitude = lng

            destination.selected_pin = selected_pin
            destination.save()

            url = reverse("destinations:destination_edit", kwargs={"pk": destination.pk})

            params = []
            if day_schedule_id:
                params.append(f"day_schedule_id={day_schedule_id}")
            if from_page:
                params.append(f"from={from_page}")
            if schedule_id:
                params.append(f"schedule_id={schedule_id}")

            if params:
                url += "?" + "&".join(params)

            return redirect(url)

    context = {
        "destination": destination,
        "pins": pins,
        "selected_pin": selected_pin,
        "day_schedule_id": day_schedule_id,
        "from_page": from_page,
        "schedule_id": schedule_id,
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
    
def get_auto_pin_color(pin_id):
    hue = (pin_id * 137) % 360
    return f"hsl({hue}, 70%, 65%)"    

def map_pin_edit(request, destination_id):
    
    destination = get_object_or_404(Destination, pk=destination_id, user=request.user)
    pins = MapPin.objects.filter(user=request.user).order_by("order", "id")
    
    day_schedule_id = request.GET.get("day_schedule_id") or request.POST.get("day_schedule_id")
    from_page = request.GET.get("from") or request.POST.get("from")
    schedule_id = request.GET.get("schedule_id") or request.POST.get("schedule_id")
    
     # GETパラメータから選択ピン取得
    selected_pin = None
    pin_id = request.GET.get("pin_id") or request.POST.get("pin_id")
    
    print("destination_id:", destination_id)
    print("pin_id:", pin_id)
    print("method:", request.method)

    if pin_id:
        selected_pin = get_object_or_404(
            MapPin,
            pk=pin_id,
            user=request.user
        )

    # 追加処理（pin_idなし）
    if request.method == "POST" and request.POST.get("action") == "add":
        form = MapPinForm(request.POST)
        if form.is_valid():
            new_pin = form.save(commit=False)
            new_pin.user = request.user
            new_pin.save()

            if not new_pin.color:
                new_pin.color = get_auto_pin_color(new_pin.id)
                new_pin.save(update_fields=["color"])
        
            url = reverse("destinations:map_destination", kwargs={"pk": destination.id})
            params = [f"pin_id={new_pin.id}"]

            if day_schedule_id:
                params.append(f"day_schedule_id={day_schedule_id}")
            if from_page:
                params.append(f"from={from_page}")
            if schedule_id:
                params.append(f"schedule_id={schedule_id}")

            if params:
                url += "?" + "&".join(params)

            return redirect(url)

    # 編集処理（pin_idあり）
    if request.method == "POST" and request.POST.get("action") != "add" and selected_pin:
        edit_form = MapPinForm(request.POST, instance=selected_pin)
        if edit_form.is_valid():
            updated_pin = edit_form.save(commit=False)
            updated_pin.user = request.user
            updated_pin.save()

            url = reverse("destinations:map_pin_edit", kwargs={"destination_id": destination.id})
            params = [f"pin_id={updated_pin.id}"]

            if day_schedule_id:
                params.append(f"day_schedule_id={day_schedule_id}")
            if from_page:
                params.append(f"from={from_page}")
            if schedule_id:
                params.append(f"schedule_id={schedule_id}")

            if params:
                url += "?" + "&".join(params)

            return redirect(url)    

    form = MapPinForm()

    return render(
        request,
        "destinations/map_pin_edit.html",
        {
            "destination": destination,
            "pins": pins,
            "form": form,
            "selected_pin": selected_pin,
            "day_schedule_id": day_schedule_id,
            "from_page": from_page,
            "schedule_id": schedule_id,
        }
    )


def map_pin_delete(request, destination_id, pin_id):
    destination = get_object_or_404(Destination, pk=destination_id, user=request.user)
    pin = get_object_or_404(MapPin, pk=pin_id, user=request.user)

    day_schedule_id = request.POST.get("day_schedule_id") or request.GET.get("day_schedule_id")
    from_page = request.POST.get("from") or request.GET.get("from")
    schedule_id = request.POST.get("schedule_id") or request.GET.get("schedule_id")

    if request.method == "POST":
        pin.delete()

        url = reverse("destinations:map_destination", kwargs={"pk": destination.id})
        params = []

        if day_schedule_id:
            params.append(f"day_schedule_id={day_schedule_id}")
        if from_page:
            params.append(f"from={from_page}")
        if schedule_id:
            params.append(f"schedule_id={schedule_id}")

        if params:
            url += "?" + "&".join(params)

        return redirect(url)

    return render(
        request,
        "destinations/map_pin_delete.html",
        {
            "destination": destination,
            "pin": pin,
            "day_schedule_id": day_schedule_id,
            "from_page": from_page,
            "schedule_id": schedule_id,
        }
    )