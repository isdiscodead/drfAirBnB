from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    # 오류로 인해 null=True 추가
    favs = models.ManyToManyField("rooms.Room", related_name="favs", blank=True)

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"
