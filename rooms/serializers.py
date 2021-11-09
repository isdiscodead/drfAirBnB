from rest_framework import serializers

from rooms.models import Room
from users.serializers import TinyUserSerializer


class RoomSerializer(serializers.ModelSerializer):
    # Room model에 있는 field 가져오기

    # name = serializers.CharField(max_length=140)
    # price = serializers.IntegerField()
    # bedrooms = serializers.IntegerField()
    # instant_book = serializers.BooleanField()

    # user 객체의 데이터를 보기 좋게, 따로 Serialize !
    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ("pk", "name", "price", "instant_book", "bedrooms", "user")


class BigRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        # exclude = ()와 동일한 코드
        fields = '__all__'
