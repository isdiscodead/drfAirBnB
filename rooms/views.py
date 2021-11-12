from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import *


# function based view
@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()[:5]  # 5개만 가져오기
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    elif request.method == "POST":
        # django는 post로 받은 json data를 python dictionary로 변환함
        # 따라서 drf view가 필요한 것!

        if not request.user.is_authenticated:   # POST 요청을 보내기 위해서는 user 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WriteRoomSerializer(data=request.data)
        print(dir(serializer))

        if serializer.is_valid():   # -> 필요한 게 없다면 false
            room = serializer.save(user=request.user)  # save() 메소드 호출 -> create or update
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class based view ( 기본 )
class ListRoomView(APIView):

    # 이런 방법으로 간단하게 유저 인증 여부, 권한 여부 확인 가능
    # authentication_classes = [authentication, TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


# Generic View
class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer


# RetireveAPIView -> 하나만 가져오기 특화!
class SeeRoomView(RetrieveAPIView):
    # queryset은 list지만, url을 통해 자동으로 일치하는 pk의 데이터 가져옴
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer
    lookup_url_kwarg = "pk"


