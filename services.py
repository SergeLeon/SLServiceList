from io import BytesIO
from PIL import Image
from mimetypes import guess_type

PIL_FORMATS = ["png", "jpeg jpg jfif", "ico", "bmp", "gif", "blp", "dds", "dib", "eps", "icns", "im", "pcx",
               "sgi", "tga", "tiff", "webp", "xbm", "ppm"]

FILE_FORMATS = {
    "Images": {},
    "Documents": {},
    "Video": {},
    "Audio": {},
}

for img_file_format in PIL_FORMATS:
    format_outputs = PIL_FORMATS[:]
    format_outputs.remove(img_file_format)

    FILE_FORMATS["Images"][img_file_format] = format_outputs


def convert(file: BytesIO, file_group, input_format, output_format) -> BytesIO:
    temp = BytesIO()
    if file_group == "Images" and input_format in PIL_FORMATS and str_in_list(PIL_FORMATS, output_format):
        img = Image.open(file)
        if output_format in ("jpeg", "ppm", "eps", ):
            img = img.convert('RGB')
        if output_format in ("xbm", ):
            img = img.convert('1')
        if output_format in ("sgi", "dds"):
            img = img.convert('RGBA')
        img.save(temp, format=output_format)
    else:
        raise ValueError(f"{input_format} or {output_format} not implemented")

    return temp


def str_in_list(in_list, string):
    for i in in_list:
        if string in i:
            return True
    return False


def transform_filename(file_name: str, file_format: str):
    splited = file_name.rsplit(".")
    return f"{splited[0]}.{file_format}"


def get_content_type(file_name):
    return guess_type(file_name, strict=True)[0]
