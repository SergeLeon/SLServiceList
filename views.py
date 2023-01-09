from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse

from .services import FILE_FORMATS, convert, get_content_type, transform_filename


def index(request):
    if request.method == "GET":
        return render(request, "index.html")

    # POST request
    if not request.FILES:
        return JsonResponse(FILE_FORMATS)

    input_file = request.FILES["file"]
    if input_file.size > 16000000:
        return HttpResponseBadRequest()

    input_info = request.POST.get("input", "")
    input_group, input_format = input_info.split(":")
    output_format = request.POST.get("output", "")

    output = convert(input_file, input_group, input_format, output_format)
    output_file = output.getvalue()
    output_file_name = transform_filename(input_file.name, output_format)

    print(get_content_type(output_file_name))
    response = HttpResponse(output_file, content_type=get_content_type(output_file_name))
    response['Content-Disposition'] = f'attachment; filename="{output_file_name}"'
    return response
