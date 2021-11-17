from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


# function view -> class based view 변경
class RoomsView(APIView):

    def get(self, request):
        rooms = Room.objects.all()[:5]  # 5개만 가져오기
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)

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
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(ReadRoomSerializer(room).data)
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


