from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import *


# 직접 Pagination 클래스를 만들면 설정 부분 생략 가능
class OwnPagination(PageNumberPagination):
    page_size = 20


# function view -> class based view 변경
class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination() # 인스턴스 생성
        rooms = Room.objects.all()
        # request를 파싱 -> paginator가 page query argument를 찾아내기 위함
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(rooms, many=True, context={'request': request}).data
        # paginated response를 return -> 이전/이후 페이지 등 사용 가능
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:  # POST 요청을 보내기 위해서는 user 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = RoomSerializer(data=request.data)
        print(dir(serializer))

        if serializer.is_valid():  # -> 필요한 게 없다면 false
            room = serializer.save(user=request.user)  # save() 메소드 호출 -> create or update
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # partial=True 옵션으로 수정하고자 하는 데이터만 보낼 수 있게 된다
            serializer = RoomSerializer(room, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            return Response()

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)

        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def room_search(request):
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

    paginator = PageNumberPagination
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
