from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "DELETE"])   # decorator를 function base view 위에 명시!
def list_rooms(request):
    # return Response -> 기본 제공 response page, 시각적으로 api 상호작용 가능
    return Response()
