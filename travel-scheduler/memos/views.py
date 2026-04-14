from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Memo

def memo_list(request):
    q = request.GET.get("q", "").strip()

    memos = Memo.objects.filter(user=request.user)

    if q:
        memos = memos.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )

    memos = memos.order_by("-updated_at", "-id")

    memo_rows = []
    for memo in memos:
        content_lines = [line.strip() for line in memo.content.splitlines() if line.strip()]
        summary = content_lines[1] if len(content_lines) >= 2 else ""

        memo_rows.append({
            "id": memo.id,
            "title": memo.title,
            "summary": summary,
        })

    return render(request, "memos/memo_list.html", {
        "q": q,
        "memo_rows": memo_rows,
        "is_shortcut": request.GET.get("shortcut") == "1",
    })


def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id, user=request.user)
    return render(request, "memos/memo_detail.html", {
        "memo": memo,
    })

def memo_edit(request):
    memo_id = request.POST.get("memo_id") or request.GET.get("memo_id")
    memo = get_object_or_404(Memo, id=memo_id, user=request.user) if memo_id else None

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        content_lines = [line.strip() for line in content.splitlines() if line.strip()]
        title = content_lines[0][:50] if content_lines else ""

        if memo:
            memo.title = title
            memo.content = content
            memo.save()
        else:
            Memo.objects.create(
                user=request.user,
                title=title,
                content=content,
            )

        return redirect("memos:memo_list")

    return render(request, "memos/memo_edit.html", {
        "memo": memo,
    })


def memo_delete(request):
    memo_id = request.POST.get("memo_id") or request.GET.get("memo_id")

    if not memo_id:
        return redirect("memos:memo_list")

    memo = get_object_or_404(Memo, id=memo_id, user=request.user)

    if request.method == "POST":
        memo.delete()
        return redirect("memos:memo_list")

    return render(request, "memos/memo_delete.html", {
        "memo": memo,
    })