from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwner
from .serializers import *


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]

        # 각각의 permission에 대한 실행 결과 리스트 반환
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        max_price = request.GET.get('max_price', None)
        min_price = request.GET.get('min_price', None)
        beds = request.GET.get('beds', None)
        bedrooms = request.GET.get('bedrooms', None)
        bathrooms = request.GET.get('bathrooms', None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms

        if lat is not None and lng is not None:
            filter_kwargs["lat__gte"] = float(lat) - 0.005
            filter_kwargs["lat__lte"] = float(lat) + 0.005
            filter_kwargs["lng__gte"] = float(lng) - 0.005
            filter_kwargs["lng__lte"] = float(lng) + 0.005

        paginator = self.paginator  # viewset에는 pagenumberpaginater 존재
        paginator.page_size = 10
        # queryset filter #
        # __lte : 작거나 같음 / __gte : 크거나 같음 / __startswith : ~로 시작
        # *filter_kwargs 로 unpack하면 key 값들이 나옴!
        # **filter_kwargs는 print는 불가능하지만 filter()에 키=값 형태로 들어가게 됨
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
