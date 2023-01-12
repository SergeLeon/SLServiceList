from django.http import HttpResponse
from django.shortcuts import render

from .services import generate


def index(request):
    if request.method == "GET":
        return render(request, "qrcoder.html")

    # POST request
    content = request.POST.get("content", "")
    print(len(content))
    correction = request.POST.get("correction", "")
    style = request.POST.get("style", "")

    output = generate(content, style, correction)
    output_file = output.getvalue()

    response = HttpResponse(output_file, content_type="Content-Type: image/png")
    response['Content-Disposition'] = 'attachment; filename=qrcode.png'
    return response
