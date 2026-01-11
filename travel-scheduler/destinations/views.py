from django.shortcuts import render

# destination_search.html  
def destination_search(request):
    q = request.GET.get("q", "")

    # 仮の検索結果（model実装に変更する）
    destinations = []

    return render(
        request,
        "destinations/destination_search.html",
        {
            "q": q,
            "destinations": destinations,
        }
    )
    
# destination_edit.html  
from django.shortcuts import render, redirect

def destination_edit(request):
    if request.method == "POST":
        # 今は保存処理なし（後で書く）
        return redirect("plans:plan_detail")

    return render(request, "destinations/destination_edit.html")



# destination_delete.html  
def destination_delete(request):
    if request.method == 'POST':
        # 今は削除処理なし（model未実装のため）
        # 削除した体で plan_detail に戻す
        return redirect('plans:plan_detail')

    # GET のときは削除確認画面を表示
    return render(
        request,
        'destinations/destination_delete.html'
    )