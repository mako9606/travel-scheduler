from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, Sum
from django.http import JsonResponse
from django.utils import timezone

from datetime import date, timedelta

from .models import Plan, DaySchedule, Schedule, Cost, CostCategory, PlanShareMember
from destinations.models import Destination

from .forms import PlanCreateForm, ScheduleForm, CostForm, CostCategoryForm

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

@login_required
def plan_edit(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)

    current_year = date.today().year
    years = range(current_year - 10, current_year + 60)
    months = range(1, 13)
    days = range(1, 32)

    if request.method == "POST":
        plan_name = request.POST.get("plan_name", "").strip()

        start_year = request.POST.get("start_year")
        start_month = request.POST.get("start_month")
        start_day = request.POST.get("start_day")

        end_year = request.POST.get("end_year")
        end_month = request.POST.get("end_month")
        end_day = request.POST.get("end_day")

        if plan_name:
            plan.plan_name = plan_name

        if start_year and start_month and start_day:
            plan.start_date = date(
                int(start_year),
                int(start_month),
                int(start_day),
            )

        if end_year and end_month and end_day:
            plan.end_date = date(
                int(end_year),
                int(end_month),
                int(end_day),
            )

        plan.save()
        return redirect("plans:plan_detail", pk=plan.pk)

    return render(request, "plans/plan_edit.html", {
        "plan": plan,
        "years": years,
        "months": months,
        "days": days,
    })

@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)

    if request.method == "POST":
        plan.delete()
        return redirect("plans:plan_list")

    return render(request, "plans/plan_delete.html", {
        "plan": plan,
    })


def plan_share(request, token):
    member = get_object_or_404(PlanShareMember, token=token)
    plan = member.plan

    is_valid = member.is_active and member.expires_at >= timezone.now()

    if request.method == "POST" and is_valid:
        action = request.POST.get("action")

        if action == "login":
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")

            if not email or not password:
                return render(request, "plans/plan_share.html", {
                    "member": member,
                    "plan": plan,
                    "is_valid": is_valid,
                    "error_message": "メールアドレスとパスワードを入力してください。",
                })

            user = authenticate(request, username=email, password=password)

            if user is None:
                return render(request, "plans/plan_share.html", {
                    "member": member,
                    "plan": plan,
                    "is_valid": is_valid,
                    "error_message": "メールアドレスまたはパスワードが正しくありません。",
                })

            login(request, user)

            request.session["shared_plan_id"] = plan.id
            request.session["shared_member_id"] = member.id
            request.session["shared_viewer_name"] = user.username

            return redirect("plans:plan_detail", pk=plan.id)


        if action == "view":
           username = request.POST.get("username", "").strip()

        if not username:
            return render(request, "plans/plan_share.html", {
                "member": member,
                "plan": plan,
                "is_valid": is_valid,
                "error_message": "アカウント名を入力してください。",
            })

        request.session["shared_plan_id"] = plan.id
        request.session["shared_member_id"] = member.id
        request.session["shared_viewer_name"] = username

        return redirect("plans:plan_detail", pk=plan.id) 
        
    return render(request, 'plans/plan_share.html', {
        'member': member,
        'plan': member.plan,
        "is_valid": is_valid,
    })

# share_revoke.html
@login_required
def share_revoke(request, member_id):
    member = get_object_or_404(PlanShareMember, pk=member_id) 
    
    if request.method == "POST":
        member.is_active = False
        member.save(update_fields=["is_active"])
        return redirect("plans:plan_detail", pk=member.plan.id)

    return render(request, "plans/share_revoke.html", {
        "member": member,
        "plan": member.plan,
    })


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
        
        # まず保存
        response = super().form_valid(form)

        # デフォルトカテゴリー作成
        CostCategory.objects.create(plan=self.object, name="入場料")
        CostCategory.objects.create(plan=self.object, name="駐車場")

        return response
    


    
class PlanDetailView(DetailView):
    model = Plan
    template_name = "plans/plan_detail.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        is_owner = request.user.is_authenticated and self.object.user == request.user
        is_shared_viewer = request.session.get("shared_plan_id") == self.object.id

        if not is_owner and not is_shared_viewer:
            return redirect("plans:plan_list")

        return super().dispatch(request, *args, **kwargs)

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
        

        total_cost = plan.costs.aggregate(total=Sum("amount"))["total"] or 0
        categories = (
            plan.cost_categories
            .annotate(total=Sum("items__amount"))
        )
        context["categories"] = categories
        context["total_cost"] = total_cost
        context["date_list"] = date_list
        
        #共有について
        share_members = plan.share_members.filter(is_active=True)

        context["share_members"] = share_members
        context["share_status"] = "有" if share_members.exists() else "無"
        
        is_owner = self.request.user.is_authenticated and plan.user == self.request.user
        is_shared_viewer = self.request.session.get("shared_plan_id") == plan.id

        context["is_owner"] = is_owner
        context["is_shared_viewer"] = is_shared_viewer
        context["shared_viewer_name"] = self.request.session.get("shared_viewer_name", "")
        
        tab_order = self.request.session.get(f"tab_order_{plan.pk}")
        context["tab_order"] = tab_order or []
        
        destination_modal = None
        destination_modal_day = None
        destination_modal_is_registered = False

        destination_modal_id = self.request.GET.get("destination_modal_id")
        day_schedule_id = self.request.GET.get("day_schedule_id")

        if destination_modal_id:
            destination_modal = Destination.objects.filter(pk=destination_modal_id).first()

        if day_schedule_id:
            destination_modal_day = DaySchedule.objects.filter(
                pk=day_schedule_id,
                plan=plan
            ).first()

        if destination_modal and destination_modal_day:
            destination_modal_is_registered = Schedule.objects.filter(
                day=destination_modal_day,
                destination=destination_modal
            ).exists()

        context["destination_modal"] = destination_modal
        context["destination_modal_day"] = destination_modal_day
        context["destination_modal_is_registered"] = destination_modal_is_registered
        
        return context
    
    
    #メモタブ編集
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        is_owner = request.user.is_authenticated and self.object.user == request.user
        if not is_owner:
            return redirect("plans:plan_detail", pk=self.object.pk)

        if "plan_memo" in request.POST:
            self.object.memo = request.POST.get("plan_memo", "").strip()
            self.object.save(update_fields=["memo"])

        return redirect(f"{reverse('plans:plan_detail', kwargs={'pk': self.object.pk})}?memo_tab=1")

# タブの順番入れ替え
@require_POST
@login_required
def tab_reorder(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)

    order = request.POST.getlist("order[]")
    request.session[f"tab_order_{plan.pk}"] = order

    return JsonResponse({"status": "ok"})


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
#　カテゴリー新規作成
@login_required
def cost_category_create(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == "POST":
        form = CostCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.plan = plan
            category.save()
            return redirect("plans:plan_detail", pk=plan.id)
    else:
        form = CostCategoryForm()

    return render(request, "plans/plan_cost_edit.html", {
        "category_form": form,
        "plan": plan,
        "mode": "category_create",
    })
    

# plan_cost_edit.html
#　カテゴリー既存編集 
@login_required
def cost_category_edit(request, pk, category_id):
    plan = get_object_or_404(Plan, pk=pk)
    category = get_object_or_404(CostCategory, pk=category_id, plan=plan)

    if request.method == "POST":
        form = CostCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("plans:plan_detail", pk=plan.id)
    else:
        form = CostCategoryForm(instance=category)

    return render(request, "plans/plan_cost_edit.html", {
        "category_form": form,
        "plan": plan,
        "category": category,
        "mode": "category_edit",
    })
    

@login_required
def cost_category_delete(request, pk, category_id):
    plan = get_object_or_404(Plan, pk=pk)
    category = get_object_or_404(CostCategory, pk=category_id, plan=plan)

    if request.method == "POST":
        category.delete()
        return redirect("plans:plan_detail", pk=plan.id)

    return render(request, "plans/cost_category_delete.html", {
        "plan": plan,
        "category": category,
    })    


# plan_cost_edit.html
#　項目編集時
@login_required
def plan_cost_edit(request, pk, cost_id=None):
    plan = get_object_or_404(Plan, pk=pk)
    
    cost = None
    if cost_id is not None:
        cost = get_object_or_404(Cost, pk=cost_id, plan=plan)

    if request.method == "POST":
        form = CostForm(request.POST, plan=plan, instance=cost)
        print("POST DATA:", request.POST)
        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.plan = plan
            cost.save()
            return redirect("plans:plan_detail", pk=plan.id)
    else:
        form = CostForm(plan=plan, instance=cost)

    return render(request, "plans/plan_cost_edit.html",{
            "form": form,
            "plan": plan,
            "cost": cost,
        })
    
@login_required
def cost_delete(request, pk, cost_id):
    plan = get_object_or_404(Plan, pk=pk)
    cost = get_object_or_404(Cost, pk=cost_id, plan=plan)
    
    if request.method == "POST":
        cost.delete()
        return redirect("plans:plan_detail", pk=plan.id)

    return render(request, "plans/plan_cost_delete.html", {
        "plan": plan,
        "cost": cost,
    })
 
    
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
   
    
def schedule_memo(request, day_id):
    day = get_object_or_404(DaySchedule, pk=day_id)
    plan = day.plan

    if request.method == "POST":
        day.memo = request.POST.get("memo", "")
        day.save(update_fields=["memo"])
        return redirect("plans:plan_detail", pk=day.plan.pk)

    return render(
        request,
        "plans/schedule_memo.html",
        {
            "day": day,
            "plan": plan,
        }
    )