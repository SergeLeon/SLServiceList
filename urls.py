from django.urls import path
from django.shortcuts import redirect
from .views import redirect_user, delete, index

urlpatterns = [
    path("", lambda request: redirect('create/')),
    path("create/", index),
    path("d/<str:short_link>/", delete),
    path("<str:short_link>/", redirect_user),
]

handler404 = "apps.cutter.views.page_not_found"
