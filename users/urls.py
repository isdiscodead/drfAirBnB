from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns = router.urls
