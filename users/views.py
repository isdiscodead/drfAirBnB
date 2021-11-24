from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet

from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.serializers import UserSerializer
from .permissions import IsSelf

import jwt


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods="POST")
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                encoded_jwt = jwt.encode({'pk': user.pk}, 'settings.SECRET_KEY', algorithm='HS256')
                return Response(data={"token": encoded_jwt, "id": user.pk})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 두 가지 이상의 접근 방식을 사용해야 하는 경우 class view가 더 적합함!
class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(serializer.data)

    # 이런 방식의 DB 수정을 put으로 할지 post로 할지는 선택임
    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user

        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()

            except room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
