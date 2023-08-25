from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
"""
API명 : 행사등록 API
설명 : 행사를 등록하는 API
작성자 : 남석현
"""
class EventCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = request.user
        request.data['user'] = user.id
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

"""
API명 : 행사 수정 및 삭제
작성자 : 남석현
"""
class EventDetailAPIView(APIView):
    def get_event(self, event_id):
        event = get_object_or_404(Event, id=event_id)
        return event
    def get(self, request, event_id, format=None):
        event = self.get_event(event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, event_id, format=None):
        event = self.get_event(event_id)
        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "check": True,
                "message": "행사가 수정되었습니다."
            }
            return Response(response_data, status=status.HTTP_200_OK)

        response_data = {
            "check": False,
            "message": "유효하지 않은 데이터입니다."
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id, format=None):
        event = self.get_event(event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)