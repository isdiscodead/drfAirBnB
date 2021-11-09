from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = "rooms"

router = DefaultRouter()
# register(url에 들어갈 이름, namespace, basename)
router.register("", viewsets.RoomViewset, basename="room")

# urlpatterns = [
    # path("list", views.ListRoomsView.as_view()),
    # path("<int:pk>/", views.SeeRoomView.as_view()),
# ]

urlpatterns = router.urls
