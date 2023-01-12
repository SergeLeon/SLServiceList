from io import BytesIO

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.constants import (ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H)
from qrcode.exceptions import DataOverflowError
from qrcode.image.styles.moduledrawers import \
    (SquareModuleDrawer, GappedSquareModuleDrawer,
     CircleModuleDrawer, RoundedModuleDrawer,
     VerticalBarsDrawer, HorizontalBarsDrawer)

DRAWERS = {
    "square": SquareModuleDrawer,
    "gsquare": GappedSquareModuleDrawer,
    "circle": CircleModuleDrawer,
    "rounded": RoundedModuleDrawer,
    "vbars": VerticalBarsDrawer,
    "hbars": HorizontalBarsDrawer,
}

CORRECTS = {
    "1": ERROR_CORRECT_L,
    "2": ERROR_CORRECT_M,
    "3": ERROR_CORRECT_Q,
    "4": ERROR_CORRECT_H,
}


def generate(content, drawer: str = "square", correction: str = "1") -> BytesIO:
    if drawer not in DRAWERS:
        drawer = "square"
    if correction not in CORRECTS:
        correction = "1"

    qr = qrcode.QRCode(
        version=None,
        error_correction=CORRECTS[correction],
        box_size=16,
        border=4,
        image_factory=StyledPilImage
    )
    qr.add_data(content)
    temp = BytesIO()

    try:
        qr.make(fit=True)
    except DataOverflowError:
        return temp

    img = qr.make_image(module_drawer=DRAWERS[drawer]())
    img.save(temp, format="png")
    return temp
