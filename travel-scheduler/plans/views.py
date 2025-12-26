from django.shortcuts import render

# Create your views here.

def plan_list(request):
    return render(request, "plans/plan_list.html")