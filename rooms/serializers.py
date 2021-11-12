from rest_framework import serializers

from rooms.models import Room
from users.serializers import TinyUserSerializer


class ReadRoomSerializer(serializers.ModelSerializer):
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
    # models와 동일, models 대신 serializers 사용
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

    def create(self, validated_data):
        # create()는 반드시 create() 호출을 반환해야 함
        return Room.objects.create(**validated_data)    # **으로 데이터 언패킹

    # validate_ 되어 있으면 자동으로 호출됨
    def validate_beds(self, beds):
        if beds < 4:
            raise serializers.ValidationError("Your house is too small")
        else:
            return beds

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        else:
            return data


# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         # exclude = ()와 동일한 코드
#         fields = '__all__'
