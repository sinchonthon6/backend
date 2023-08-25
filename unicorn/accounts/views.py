import os
from typing import Union
import requests

from django.contrib.auth import get_user_model

from rest_framework.views import APIView, View
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import redirect

from .serializers import UserSerializer



User = get_user_model()

REDIRECT_URI = 'http://localhost:3000/auth'
ACCESS_TOKEN_URI = 'https://kauth.kakao.com/oauth/token'
USER_INFO_URI = 'https://kapi.kakao.com/v2/user/me'

class KakaoSignInView(View):
    def get(self, request):
        app_key = '0359e71d1e648b5199a68866b3ccaa32'
        redirect_uri = 'http://localhost:3000/auth'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'

        return redirect (
            f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
        )

class OAuthTokenObtainView(APIView):

    allowed_methods = ('POST',)
    permission_classes = (AllowAny,)

    def request_access_token(self, access_code: str) -> dict:
        return requests.post(
            ACCESS_TOKEN_URI,
            headers={
                'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
            data={
                'grant_type': 'authorization_code',
                'client_id': '0359e71d1e648b5199a68866b3ccaa32',
                'redirect_uri': REDIRECT_URI,
                'code': access_code,
            }
        )

    def get_access_token_error(self, response: dict) -> str:
        response.get('error')

    def reqeust_user_info(self, access_token) -> Union[str, None]:
        return requests.get(
            USER_INFO_URI,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

    def post(self, request) -> Response:
        # OAuth 제공 업체 이름, 요청 body의 유효성 검사
        access_code = request.data.get('code')
        # access code <-> access token 교환
        response = self.request_access_token(access_code)
        if response.status_code != 200:
            return Response(
                {
                    'detail': self.get_access_token_error(response.json())
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        access_token = response.json()['access_token']

        # OAuth 제공 업체 provider에게 사용자 정보 요청
        response = self.reqeust_user_info(access_token)
        if response.status_code != 200:
            return Response(
                {
                    'detail': 'Email is not found'
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        user_info = response.json()
        print(user_info)
        oauth_id = user_info["id"]
        email = user_info["kakao_account"]["email"]
        print(email)

        # OAuth 인증으로 가입한 사용자 정보 탐색
        try:
            # 동일한 id를 사용하는 사용자가 db에 있는 경우에
            user = User.objects.get(email=email) # email이 email인 객체 하나를 반환
        # 기존에 가입된 유저가 없으면 임시로 저장하고 새로 가입
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, password=None, oauth_id=oauth_id)
            user.is_register = True

        # JWT 발급, 응답
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'is_register': user.is_register,
            },
            status=status.HTTP_200_OK,
        )

class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    #로그인
    def get(self, request):
        return Response(UserSerializer(request.user).data)

def get_user_id(token):
    decoded_token = AccessToken(token)
    user_id = decoded_token.payload.get('user_id')
    return user_id