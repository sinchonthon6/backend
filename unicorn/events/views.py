from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer

# Create your views here.
"""
API명 : 행사등록 API
설명 : 행사를 등록하는 API
작성자 : 남석현
"""
class EventCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "check": True,
                "message": "행사가 등록되었습니다."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        response_data = {
            "check": False,
            "message": "유효하지 않은 데이터입니다."
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

