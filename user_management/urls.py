from django.urls import path

from . import views

urlpatterns = [
    path('v1/login', views.UserLoginApi.as_view(), name='user-login'),  # login with password - test case written
    path('v1/list', views.UserFilterApi.as_view(), name='user_list'),  # See the list of User
    path('v1/detail/<int:pk>', views.UserDetailApi.as_view(), name='user_details'),  # See the detail of particular user
    path('v1/short-info/<int:pk>', views.UserShortInfoApi.as_view(), name='user_short_details'),
    # See the short information of User
    path('v1/profile/<int:pk>', views.UserProfileApi.as_view(), name='user_profile'),
    # see the details of the User with roles and privileges

    path('v1/register', views.RegisterApi.as_view(), name='register'),
    # A new user can register and got email notifications.
    path('v1/register/admin', views.RegisterUserApi.as_view(), name='new_register'),
    # this is for the admin registration where a user is considered as admin (Some Logic is still left)
    path('v1/<int:pk>', views.UserModifyApi.as_view(), name='user_modify'),
    # This is for the user details change api not recommended to change the password by using this endpoint

    path('v1/status/<int:pk>', views.UserStatusApiView.as_view(), name='user_status'),
    # this is for to change the user status.

    path('v1/password/change', views.UserChangePasswordApi.as_view(), name='user_password_change'),
    # Looking into the password change by the User when user wants to change the password.

    path('v1/password/forgot/<str:email>', views.UserForgotPasswordApi.as_view(), name='user_password_forgot'),
    path('v1/password/verify/otp', views.UserOtpVerifyApi.as_view(), name='password_otp_verify'),
    path('v1/reset/password', views.UserPasswordResetApi.as_view(), name='user_password_reset'),
    # these above 3 endpoint is for the password reset.

    path('v1/json-info', views.UserJsonDataAPI.as_view(), name='user_details_json'),
    path('v1/token/generate', views.GenerateTokenView.as_view(), name='generate-token'),
    path('v1/token/reset/<str:pk>', views.ResetTokenView.as_view(), name='reset-token')
]
