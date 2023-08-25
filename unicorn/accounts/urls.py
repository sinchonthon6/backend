from django.contrib import admin
from django.urls import path
from .views import OAuthTokenObtainView, KakaoSignInView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView

app_name='accounts'      

urlpatterns = [
    path('kakao/token/', OAuthTokenObtainView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserInfoView.as_view(), name='user_info'),
    path('kakao/signin/', KakaoSignInView.as_view(), name='kakao_signin')
]