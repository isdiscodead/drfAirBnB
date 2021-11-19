from django.conf import settings
from users.models import User
from rest_framework import authentication
from rest_framework import exceptions
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token is None:
                return None
            # X-JWT 부분, token string으로 분리
            xjwt, jwt_token = token.split(" ")
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms='HS256')
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            return user
        except (ValueError, User.DoeseNotExists):
            return None

        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")
