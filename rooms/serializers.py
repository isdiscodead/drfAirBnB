from rest_framework import serializers

from rooms.models import Room
from users.serializers import RelatedUserSerializer


class ReadRoomSerializer(serializers.ModelSerializer):
    # Room model에 있는 field 가져오기
    # name = serializers.CharField(max_length=140) ...

    # user 객체의 데이터를 보기 좋게, 따로 Serialize ! ( Nested )
    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

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


# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         # exclude = ()와 동일한 코드
#         fields = '__all__'
