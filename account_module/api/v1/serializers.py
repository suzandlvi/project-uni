import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account_module.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer with password checkup"""

    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True
    )
    password1 = serializers.CharField(
        max_length=68, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ["email", "password", "password1", "avatar"]

    def validate(self, data):
        if data["password"] != data["password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        if len(data["password"]) < 8:
            return serializers.ValidationError('رمز عبور نمیتواند کمتر از 8 کارکتر باشد')
        return data

    def create(self, validated_data):
        validated_data.pop("password1")
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer to manage extra user info"""
    full_name = serializers.ReadOnlyField(source='__str__')
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)

    # avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only_fields = ["email", "is_superuser", "is_staff", "is_active"]
        fields = [
            "email",
            "full_name",
            "avatar",
            # "avatar_url",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

    # def get_avatar_url(self, instance):
    #     request = self.context.get('request')
    #     avatar_url = instance.avatar.url
    #     return request.build_absolute_uri(avatar_url)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "user is not verified"})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # if not self.user.is_verified:
        #     raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True, min_length=8)
#     new_password = serializers.CharField(required=True, min_length=8)
#     new_password1 = serializers.CharField(required=True, min_length=8)
#
#     def validate(self, attrs):
#         if attrs.get("new_password") != attrs.get("new_password1"):
#             raise serializers.ValidationError(
#                 {"detail": "new_password with new_password1 is not match"}
#             )
#         # try:
#         #     validate_password(attrs.get("new_password"))
#         # except exceptions.ValidationError as e:
#         #     raise serializers.ValidationError({"new_password": list(e.messages)})
#         return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        return super().validate(attrs)


class PasswordResetRequestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "There is no user with provided email"})
        attrs["user"] = user
        return super().validate(attrs)


class PasswordResetTokenVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)

    class Meta:
        model = User
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as identifier:
            return serializers.ValidationError({'detail': 'Token expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise serializers.ValidationError({'detail': 'Token invalid'})

        attrs["user"] = user
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    password1 = serializers.CharField(
        min_length=6, max_length=68, write_only=True)

    class Meta:
        fields = ['password', 'password1', 'token']

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError(
                {"details": "Passwords does not match"}
            )
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            user.set_password(password)
            user.save()

            return super().validate(attrs)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
