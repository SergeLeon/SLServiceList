from django.shortcuts import render, redirect

from .services import create_redirection, deactivate_redirection, get_full_link


def index(request):
    if request.method == 'GET':
        return render(request, "cutter.html")

    # POST request
    full_link = request.POST.get("full_link", "")
    short_link = request.POST.get("short_link", "")
    host = request.POST.get("host", "")
    datetime = request.POST.get("datetime", "")
    count = request.POST.get("count", "")

    response = create_redirection(
        full_link=full_link,
        short_link=short_link,
        host=host,
        delete_at=datetime,
        redirect_limit=count)

    return render(
        request,
        "message.html",
        response
    )


def redirect_user(request, short_link):
    full_link = get_full_link(short_link)
    if full_link:
        return redirect(full_link)
    return page_not_found(request)


def delete(request, short_link):
    response = deactivate_redirection(short_link=short_link)
    return render(
        request,
        "message.html",
        response
    )


def page_not_found(request, exception=None):
    return render(
        request,
        "message.html",
        {"title": "404 Page not found",
         "description": "The requested link has expired or the link was entered incorrectly"},
        status=404
    )
