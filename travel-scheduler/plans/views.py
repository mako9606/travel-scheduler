from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views import View
from django.views.generic import DeleteView
from django.db.models import Max

from datetime import date, timedelta

from .models import Plan
from .forms import PlanCreateForm

from django.views.decorators.http import require_POST
from django.http import JsonResponse



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
    
    
class PlanDetailView(LoginRequiredMixin, DeleteView):
    model = Plan
    template_name = "plans/plan_detail.html"

@require_POST
@login_required
def plan_reorder(request):
    ids = request.POST.getlist("order[]")
    
    for index, plan_id in enumerate(ids):
        Plan.objects.filter(id=plan_id, user=request.user)\
            .update(order=index)
            
    return JsonResponse({"status":"ok"})         


# plan_cost_edit.html
def plan_cost_edit(request):
    return render(
        request,
        "plans/plan_cost_edit.html",
        {
            # 仮データ（あとで削除OK）
            "object": {
                "plan_name": "☆☆旅行"
            }
        }
    )
    