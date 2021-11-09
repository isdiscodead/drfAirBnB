from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


# function based view
@api_view(["GET", "DELETE"])   # decorator를 function base view 위에 명시!
def list_rooms(request):
    rooms = Room.objects.all()
    # return Response -> 기본 제공 response page, 시각적으로 api 상호작용 가능
    serialized_rooms = RoomSerializer(rooms, many=True) # many 옵션으로 list
    return Response(data=serialized_rooms.data)


# class based view
class ListRoomView(APIView):

    # 이런 방법으로 간단하게 유저 인증 여부, 권한 여부 확인 가능
    # authentication_classes = [authentication, TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer