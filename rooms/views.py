from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


@api_view(["GET", "DELETE"])   # decorator를 function base view 위에 명시!
def list_rooms(request):
    rooms = Room.objects.all()
    # return Response -> 기본 제공 response page, 시각적으로 api 상호작용 가능
    serialized_rooms = RoomSerializer(rooms, many=True) # many 옵션으로 list
    return Response(data=serialized_rooms.data)
