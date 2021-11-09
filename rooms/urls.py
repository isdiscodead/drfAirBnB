from django.conf import settings
from django.urls import path, include

from . import views

app_name = "rooms"

urlpatterns = [
    path("list", views.ListRoomsView.as_view()),
    path("<int:pk>/", views.SeeRoomView.as_view()),
]
