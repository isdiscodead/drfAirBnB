from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    # Room model에 있는 field 가져오기
    name = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    instant_book = serializers.BooleanField()