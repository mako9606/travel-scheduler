from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.views.generic import DeleteView

from datetime import timedelta

#from .models import Plan

def plan_list(request):
    return render(request, "plans/plan_list.html")



#class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    template_name = "plans/plan_create.html"
    fields = ['plan_name', 'start_date', 'end_date']
    
    def get_success_url(self):
        return reverse("plans/plan_detail", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
#↑models.py作成したら使って↓を消す
     
class PlanCreateView(View):
    def get(self, request):
        return render(request, "plans/plan_create.html")
    
    
#class PlanDetailView(DeleteView):
    #model = Plan
    #template_name = "plans/plan_detail.html"
#↑models.py作成したら使って↓を消す

class PlanDetailView(View):
    def get(self, request):
        return render(request, "plans/plan_detail.html")


# 日付タブの自動作成
def plan_detail(request):
    start = date(2025, 1, 1)
    end = date(2025, 1, 3)
    
    date_list = []
    d = start
    while d <= end:
        date_list.append(d.strftime('%-m/%-d'))
        d += timedelta(days=1)
        
    return render(request, "plans/plan_create.html",{
        "date_list": date_list,
    })    
    