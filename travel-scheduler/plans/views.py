from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Sum
from django.http import JsonResponse


from datetime import date, timedelta

from .models import Plan, DaySchedule, Schedule, Cost
from destinations.models import Destination

from .forms import PlanCreateForm, ScheduleForm, CostForm

from django.views.decorators.http import require_POST
from django.http import JsonResponse

import json

# plan_list.html
@login_required
def plan_list(request):
    plans = Plan.objects.filter(user=request.user).order_by("order")
    return render(
        request,
        "plans/plan_list.html",
        {"plans": plans}
    )

def plan_edit(request):
    return render(request, 'plans/plan_edit.html')

def plan_delete(request):
    return render(request, 'plans/plan_delete.html')

def plan_share(request):
    return render(request, 'plans/plan_share.html')

def share_revoke(request):
    return render(request, 'plans/share_revoke.html')


# plan_create.html
class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanCreateForm
    template_name = "plans/plan_create.html"
    
    def get_success_url(self):
        return reverse("plans:plan_detail", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        max_order = (
            Plan.objects
            .filter(user=self.request.user)
            .aggregate(Max("order"))["order__max"]
            or 0
        )
        form.instance.order = max_order + 1
        
        return super().form_valid(form)
    


    
class PlanDetailView(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "plans/plan_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        plan = self.object
        # 各日付を作る
        date_list = []
        if plan.start_date and plan.end_date:
            current = plan.start_date
            while current <= plan.end_date:
                date_list.append(current)
                current += timedelta(days=1)
                
        # 旅行期間の全日付に対して DaySchedule を必ず作る
        for d in date_list:
            DaySchedule.objects.get_or_create(
                plan=plan,
                date=d
            )

        # 改めて全DayScheduleを取得
        days_qs = DaySchedule.objects.filter(plan=plan).order_by("date")

        # 日付 → DaySchedule の辞書
        days_by_date = {d.date: d for d in days_qs} 
      
        # 旅行期間の全日付に対して,DayScheduleがあればそれをセット、なければNoneをセット
        schedule_rows = []
        for d in date_list:
            day = days_by_date.get(d)

            if day:
                schedules_qs = (
                    Schedule.objects
                    .filter(day=day)
                    .order_by("order")
                )
                # order 未初期化（0）のものだけ、arrival_time順で初期化
                zero_order_schedules = (
                    Schedule.objects
                    .filter(day=day, order=0)
                    .order_by("arrival_time")
                )

                if zero_order_schedules.exists():
                    for idx, s in enumerate(zero_order_schedules):
                        s.order = idx
                        s.save(update_fields=["order"])
                        
                    schedules = (
                        Schedule.objects
                        .filter(day=day)
                        .order_by("order")
                    )
                    print(
                        "DEBUG",
                        "date:", d,
                        "day_id:", day.id if day else None,
                        "schedule_day_ids:", list(schedules.values_list("day_id", flat=True)),
                    )
 
                
                else:
                    schedules = schedules_qs
            else:
                schedules = []
            
            schedule_rows.append({
                "date": d,
                "day": day,
                "schedules": schedules,
            })
        context["schedule_rows"] = schedule_rows
        

        total_cost = plan.costs.aggregate(
            total=Sum("amount")
        )["total"] or 0
        context["total_cost"] = total_cost

        context["date_list"] = date_list
        return context


# プランの順番入れ替え
@require_POST
@login_required
def plan_reorder(request):
    ids = request.POST.getlist("order[]")
    
    for index, plan_id in enumerate(ids):
        Plan.objects.filter(id=plan_id, user=request.user)\
            .update(order=index)
            
    return JsonResponse({"status":"ok"})         


# plan_cost_edit.html
@login_required
def plan_cost_edit(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == "POST":
        form = CostForm(request.POST)
        print("POST DATA:", request.POST)
        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.plan = plan
            cost.save()
            return redirect("plans:plan_detail", pk=plan.id)
    else:
        form = CostForm()

    return render(
        request,
        "plans/plan_cost_edit.html",
        {
            "form": form,
            "plan": plan,
        }
    )
    
    
# schedule_edit.html
# 新規追加時
def schedule_create(request):
    print("---- schedule_create start ----")
    print("method:", request.method)

    print("POST day_schedule_id:", request.POST.get("day_schedule_id"))
    print("GET  day_schedule_id:", request.GET.get("day_schedule_id"))

    print("POST destination_id:", request.POST.get("destination_id"))
    print("GET  destination_id:", request.GET.get("destination_id"))
    
    day_schedule_id = request.POST.get("day_schedule_id") or request.GET.get("day_schedule_id")
    destination_id = request.POST.get("destination_id") or request.GET.get("destination_id")

    print("決定 day_schedule_id:", day_schedule_id)
    print("決定 destination_id:", destination_id)
    print("---- schedule_create end ----")
    
    day_schedule = get_object_or_404(DaySchedule, pk=day_schedule_id)
    destination = get_object_or_404(Destination, pk=destination_id)
    
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        print("POST DATA:", request.POST)

        if form.is_valid():
            print("FORM VALID")
            schedule = form.save(commit=False)
            schedule.day = day_schedule
            schedule.destination = destination
            last_order = (
                Schedule.objects
                .filter(day=day_schedule)
                .aggregate(max_order=Max("order"))
                ["max_order"]
            )
            schedule.order = (last_order or 0) + 1
            schedule.save()

            return redirect(
                reverse("plans:plan_detail", kwargs={"pk": day_schedule.plan.id})
                + f"?day_schedule_id={day_schedule.id}"
            )     
    else:
        form = ScheduleForm()

    return render(
        request,
        "plans/schedule_edit.html",
        {
            "form": form,
            "schedule": None,
            "day_schedule": day_schedule,
            "destination": destination,
            "plan": day_schedule.plan, 
        }
    )
    
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    day_schedule = schedule.day

    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()    
            return redirect(
                reverse("plans:plan_detail", kwargs={'pk': day_schedule.plan.id})
                + f"?day_schedule_id={day_schedule.id}"
            )
        
        return render(request, "plans/schedule_edit.html", {
            "form": form,
            "schedule": schedule,
            "day_schedule": day_schedule,
        })
    
    else:
        form = ScheduleForm(instance=schedule)

    return render(
        request,
        "plans/schedule_edit.html",
        {
            "form": form,
            "schedule": schedule,
            "day_schedule": day_schedule,
        }
    )

#目的地の順番入れ替え　   
@require_POST
@login_required
def schedule_reorder(request):
    ids = request.POST.getlist("order[]")
    day_id = request.POST.get("day_id")

    for index, schedule_id in enumerate(ids):
        Schedule.objects.filter(
            id=schedule_id,
            day_id=day_id
        ).update(order=index)

    return JsonResponse({"status": "ok"})  
   
    
def schedule_memo(request):
    return render(request, "plans/schedule_memo.html")