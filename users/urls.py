from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    Me,
    Users,
    PublicUser,
    ChangePassword,
    LogIn,
    LogOut,
    PublicUserReviews,
    JWTLogIn,
    GithubLogIn,
    KakaoLogIn,
)

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", JWTLogIn.as_view()),
    path("github", GithubLogIn.as_view()),
    path("kakao", KakaoLogIn.as_view()),
    path("@<str:username>", PublicUser.as_view()),
    path("@<str:username>/reviews", PublicUserReviews.as_view()),
]

# from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
# from . import views
# #from . import views 코딩 시 로컬에러 발생 > 지역변수로 코딩 진행
# from .views import Me, Users, ChangePassword, PublicUser, LogIn, LogOut, JWTLogIn

# urlpatterns = [
#     path("", Users.as_view()),
#     path("me", Me.as_view()),
#     path("change-password", ChangePassword.as_view()),
#     path("log-in", LogIn.as_view()),
#     path("log-out", LogOut.as_view()),
#     path("token-login", obtain_auth_token),
#     path("jwt-login", JWTLogIn.as_view()),
#     path("token-login", obtain_auth_token),
#     path("github", views.GithubLogIn.as_view()),
#     path("kakao", views.KakaoLogIn.as_view()),
#     path("@<str:username>", PublicUser.as_view()),
# ]
