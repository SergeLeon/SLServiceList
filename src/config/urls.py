from django.urls import path, include
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=static('favicon.ico'))),
    path('', lambda request: render(request, "index.html")),
    path('r/', include("apps.cutter.urls")),
    path('c/', include("apps.converter.urls")),
    path('q/', include("apps.qrcoder.urls")),
]
