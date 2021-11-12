from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


# function view -> class based view 변경
class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()[:5]  # 5개만 가져오기
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:  # POST 요청을 보내기 위해서는 user 필요
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = WriteRoomSerializer(data=request.data)
        print(dir(serializer))

        if serializer.is_valid():  # -> 필요한 게 없다면 false
            room = serializer.save(user=request.user)  # save() 메소드 호출 -> create or update
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = ReadRoomSerializer(room).data
            return Response(data=serializer)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


