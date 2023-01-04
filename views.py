from django.http import HttpResponse
from django.shortcuts import render, redirect

from .services import create_redirection, deactivate_redirection, get_full_link


def index(request):
    if request.method == 'POST':
        print(request.POST)
        full_link = request.POST.get("full_link")

        short_link = request.POST.get("short_link")

        datetime = request.POST.get("datetime", None)
        datetime = datetime if datetime else None

        count = request.POST.get("count", None)
        count = count if count else None

        a = create_redirection(
            full_link=full_link,
            short_link=short_link,
            delete_at=datetime,
            redirect_limit=count)
        return HttpResponse(f"{a}")

    return render(request, "index.html")


def redirect_user(request, short_link):
    full_link = get_full_link(short_link)
    if full_link:
        return redirect(full_link)
    else:
        return HttpResponse("Ссылка недействительна")


def delete(request, short_link):
    a = deactivate_redirection(short_link=short_link)
    return HttpResponse(f"{a}")
