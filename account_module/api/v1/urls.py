from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # register urls
    path("register/", views.RegisterApiView.as_view(), name="register"),

    # reset password and sending email urls
    # path("password-change", views.ChangePasswordAPIView.as_view(), name="change_password_api", ),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("reset-password/", views.PasswordResetRequestEmailApiView.as_view(), name="reset-password-request"),
    path("reset-password/validate-token/", views.PasswordResetTokenValidateApiView.as_view(), name="reset-password-validate"),
    path("reset-password/set-password/", views.PasswordResetSetNewApiView.as_view(), name="reset-password-confirm"),

    # token authorization
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token_login_api"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token_logout_api"),

    # jwt authorization
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair", ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # get user urls
    path("user/profile/", views.ProfileApiView.as_view(), name="profile"),
]
