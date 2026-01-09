from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.views.generic import DeleteView

from datetime import date, timedelta

#from .models import Plan

def plan_list(request):
    return render(request, "plans/plan_list.html")

def plan_edit(request):
    return render(request, 'plans/plan_edit.html')

def plan_delete(request):
    return render(request, 'plans/plan_delete.html')

def plan_share(request):
    return render(request, 'plans/plan_share.html')


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


# 日付タブの自動作成（models作成したら変更？）
class PlanDetailView(View):
    def get(self, request):
        start = date(2025, 1, 1)
        end = date(2025, 1, 3)
    
        date_list = []
        current = start
        while current <= end:
            date_list.append(current)
            current += timedelta(days=1)
        
        context = {
            "date_list": date_list,
        }   
        return render(request, "plans/plan_detail.html", context)




    