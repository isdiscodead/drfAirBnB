from rest_framework import serializers

from rooms.models import Room
from users.serializers import RelatedUserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()
    # method name을 get_필드명으로 안 할 경우 method_name="" 속성 사용
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified", "created")
        read_only_fields = ('user', 'id', 'created', 'updated')

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

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False


# class BigRoomSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Room
#         # exclude = ()와 동일한 코드
#         fields = '__all__'
