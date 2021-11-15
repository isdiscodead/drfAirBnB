from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    # 다른 버전, v1 & v2 폴더로 관리도 가능
    # path("api/v2/rooms/", include("rooms.urls_v2")),
    path("api/v1/users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
