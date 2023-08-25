from django.shortcuts import render, get_object_or_404
from rest_framework import views
from django.db.models import Q
from events.models import Event
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .serializers import Event_Serializer
import re
from rest_framework.permissions import IsAuthenticated
from homes.serializers import EventSerializer
from rest_framework.permissions import AllowAny


class SearchView(views.APIView):
    def get(self, request):
        keyword=request.data['keyword']

        clean_search_query = re.sub(r'[^\w\s]', '', keyword)
        keywords = clean_search_query.split()
        
        print (keywords)
        qs_list = []
        current_date = datetime.now().date()
        for keyword in keywords:
            qs = Event.objects.filter(Q(title__icontains=keyword) | Q(circle_name__icontains=keyword))
            print(qs)
            for event in qs:
                if event.finish_day >= current_date:
                    event.dday = (event.finish_day - current_date).days
                    qs_list.append(event)

        qs_list=list(set([qs for qs in qs_list]))
        qs_list = sorted(qs_list, key=lambda event: event.start_day)

        # result = list(final_qs.values('event_id', 'title', 'img', 'start_day', 'finish_day', 'school', 'category', 'dday'))
        result=EventSerializer(qs_list, many=True)
        return JsonResponse({'check':True, 'data': result.data}, status=status.HTTP_200_OK)

    # return JsonResponse({'check':True, 'data': []}, status=status.HTTP_200_OK)

class EventDetailsView(APIView):
    # permission_classes = [IsOwnerOrReadOnly]
    permission_classes = [AllowAny]

    def get(self, request, event_id, format=None):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = Event_Serializer(event,context={'request': request})
        user_has_permission = IsOwnerOrReadOnly().has_object_permission(request, None, event)
        
        response_data = {
            "check":True,
            "data": serializer.data,
            # "permission": user_has_permission
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK)



