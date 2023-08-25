from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from events.models import Event
from rest_framework.response import Response
import random
from .serializers import *
from django.db.models import Q
from datetime import date

# Create your views here.



class HomeView(views.APIView):
    def get(self, request):
        # 랜덤 추천
        current_date = date.today()  # 오늘 날짜
        all_events = Event.objects.all()
        events=all_events.filter(finish_day__gte=current_date)
        ran_size = min(6, len(events))  # 리스트 크기보다 크지 않은 값을 선택
        random_events = random.sample(list(events), ran_size)
        random_events_seri = EventSerializer(random_events,many=True)
        return Response({'check':True, 'data': random_events_seri.data}, status=status.HTTP_200_OK)
    
class EventListView(views.APIView):
    def get(self, request):
        category=request.data['category']
        school =request.data['school']
        start=request.data['start']
        finish=request.data['finish']

        current_date = date.today()
        events = Event.objects.all().filter(finish_day__gte=current_date)
        
        if category!="all":
            events =events.filter(category=category)
        if school!="all":
            events =events.filter(school=school)
        if start!="all":
            events =events.filter(finish_day__gte=start)
        if finish!="all":
            events =events.filter(start_day__lte=finish)
        
        events =events.order_by('start_day')

        serializer=EventSerializer(events,many=True)

        return Response({'check':True, 'data': serializer.data}, status=status.HTTP_200_OK)
    

