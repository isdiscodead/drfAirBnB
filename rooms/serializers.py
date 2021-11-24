from rest_framework import serializers

from rooms.models import Room
from users.serializers import RelatedUserSerializer


class RoomSerializer(serializers.ModelSerializer):
    # create 시에 user를 직접 작성할 수 없도록 read_only 속성
    user = RelatedUserSerializer(read_only=True)
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

    def create(self, validated_data):
        # serializer는 자체적으로 context를 받아오고, 이를 통해 request 사용 가능
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room