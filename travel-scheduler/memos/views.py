from django.shortcuts import render

# Create your views here.
def memo_list(request):
    return render(request, "memos/memo_list.html")

def memo_detail(request):
    return render(request, "memos/memo_detail.html")

def memo_edit(request):
    return render(request, "memos/memo_edit.html")

def memo_delete(request):
    return render(request, "memos/memo_delete.html")