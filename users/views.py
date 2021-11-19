from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rooms.models import Room
from rooms.serializers import RoomSerializer
from users.models import User
from users.serializers import UserSerializer

import jwt
from django.conf import settings


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode({'pk': user.pk}, 'settings.SECRET_KEY', algorithm='HS256')
            return Response(data={"token": encoded_jwt})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MeView(APIView):

    # 이 view 전체에 필요한 permission들을 넣는 array
    # function based view에서 사용하기 위해서는
    # @api_view decorator와 @permission_classes([]) 사용
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
