from django.urls import path
from .views import RegisterAPIView,CurrentUserAPIView,TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("register/",RegisterAPIView.as_view(),name="register"),
    path("user/",CurrentUserAPIView.as_view(),name="current-user"),
    path("token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token-refresh"),
]
