from django.urls import path
from .views import redirect_user, delete, index

urlpatterns = [
    path("", index),
    path("d/<str:short_link>/", delete),
    path("<str:short_link>/", redirect_user),
]
