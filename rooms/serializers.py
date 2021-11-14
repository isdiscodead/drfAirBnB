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

    # validate_ 되어 있으면 자동으로 호출됨
    def validate_beds(self, beds):
        if beds < 4:
            raise serializers.ValidationError("Your house is too small")
        else:
            return beds

    def validate(self, data):
        # instance 객체가 있다면 update, 없다면 create임!
        if self.instance:
            check_in = data.get("chech_in", self.instance.check_in)
            check_out = data.get("chech_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")

        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between change.")

        return data

    def create(self, validated_data):
        # create()는 반드시 create() 호출을 반환해야 함
        return Room.objects.create(**validated_data)    # **으로 데이터 언패킹

    def update(self, instance, validated_data):
        # instance가 존재하기 때문에 save()에서 구분 가능
        # data를 get하되, default 값으로 이전에 존재하던 값 넣어주기
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get("instant_book", instance.instant_book)

        instance.save()
        return instance

# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         # exclude = ()와 동일한 코드
#         fields = '__all__'
