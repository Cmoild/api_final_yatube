from rest_framework_simplejwt.serializers import (
    TokenVerifySerializer, TokenRefreshSerializer
)
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import (
    RefreshToken, TokenError, UntypedToken
)


class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            UntypedToken(attrs["token"])
        except TokenError:
            raise AuthenticationFailed(
                detail="Token is invalid or expired",
                code="token_not_valid"
            )
        return {}


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs['refresh']

        try:
            token = RefreshToken(refresh)
            data = {"access": str(token.access_token)}
            return data
        except TokenError:
            raise AuthenticationFailed(
                detail="Token is invalid or expired",
                code="token_not_valid"
            )
