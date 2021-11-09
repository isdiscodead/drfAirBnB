from django.conf import settings
from django.urls import path, include

from . import views

app_name = "rooms"

urlpatterns = [
    path("list", views.ListRoomsView.as_view())
]
