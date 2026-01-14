from django.shortcuts import render

# Create your views here.
def memo_list(request):
    return render(request, "memos/memo_list.html")