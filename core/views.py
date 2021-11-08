import json
from django.core import serializers
from django.http import HttpResponse
from rooms.models import Room


def list_rooms(request):
    rooms = Room.objects.all()  # string 형태
    # rooms_json = []
    # for room in rooms:
    #    rooms_json.append(json.dumps(room))

    # Django Queryset -> Json 배열 바로 변환 불가능하므로 Serializer 사용
    data = serializers.serialize("json", Room.objects.all())
    response = HttpResponse(content=data)
    # 반드시 직렬화 및 검증 필요함 ( serialize/deserialize )

    return response
