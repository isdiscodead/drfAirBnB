from rest_framework import serializers

from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "avatar", "superhost", )


class UserSerializer(serializers.ModelSerializer):

    # 조회 시에 password를 볼 수 없도록 write_only 속성
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "avatar", "superhost", "password", "username", "first_name", "last_name", "email")
        read_only_fields = ("id", "superhost", "avatar")

    def validate_first_name(self, value):
        return value.upper()

    def create(self, validated_data):
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
