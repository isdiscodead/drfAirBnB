from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets, views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomsView.as_view()),
    path("search/", views.room_search),
    path("<int:pk>/", views.RoomView.as_view()),
]


# router = DefaultRouter()
# register(url에 들어갈 이름, namespace, basename)
# router.register("", viewsets.RoomViewset, basename="room")
# urlpatterns = router.urls
