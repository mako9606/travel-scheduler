from django.shortcuts import render


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
