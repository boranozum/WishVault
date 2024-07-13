from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework import status

from account.models import GlobalPermission
from account.serializers.user import UserSerializer
from base.permissions import grant_permission_to_user
from base.response import RestResponse


class RegisterView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            user_serializer = UserSerializer(data=request.data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        except Exception as e:
            return RestResponse(
                status=status.HTTP_400_BAD_REQUEST,
                message=str(e)
            )
        finally:
            del request.data["confirm_password"]

        token_serializer = self.get_serializer(data={
            **user_serializer.data,
            "password": request.data["password"]
        })
        try:
            token_serializer.is_valid(raise_exception=True)
            request.user = get_user_model().objects.get_by_natural_key(token_serializer.initial_data[token_serializer.username_field])
            grant_permission_to_user(
                request.user,
                GlobalPermission.PERMISSION_PRODUCT_MANAGEMENT,
                GlobalPermission.PERMISSION_COMMERCE_SITE_MANAGEMENT,
            )
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            raise e
        finally:
            del request.data["password"]

        return RestResponse(
            status=status.HTTP_200_OK,
            content=token_serializer.validated_data,
        )


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            request.user = get_user_model().objects.get_by_natural_key(serializer.initial_data[serializer.username_field])
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            raise e
        finally:
            del request.data["password"]

        return RestResponse(
            status=status.HTTP_200_OK,
            content=serializer.validated_data,
        )


class LoginRefreshView(TokenRefreshView):
    pass


class LogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        try:
            request.user = get_user_model().objects.get_by_natural_key(request.data["username"])
        except:
            pass
        return super().post(request, *args, **kwargs)