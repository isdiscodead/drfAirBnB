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
        exclude = ("modified",)


class WriteRoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField(help_text="USD per night")
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)


# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         # exclude = ()와 동일한 코드
#         fields = '__all__'
