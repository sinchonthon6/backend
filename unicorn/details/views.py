from django.shortcuts import render
from events.models import Event
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .serializers import EventSerializer
import re

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        
        if search_query:
            #문자, 숫자 제외 처리해주기
            clean_search_query = re.sub(r'[^\w\s]', '', search_query)
            keywords = clean_search_query.split()
            
            qs_list = []
            current_date = datetime.now().date()
            for keyword in keywords:
                qs = Event.objects.filter(title__icontains=keyword)
                for event in qs:
                    if event.finish_day >= current_date:
                        event.dday = (event.finish_day - current_date).days
                        qs_list.append(event)

            final_qs = qs_list[0]
            for qs in qs_list[1:]:
                final_qs = final_qs & qs

            # final_qs = final_qs.order_by('-created_at')

            result = list(final_qs.values('event_id', 'title', 'img', 'start_day', 'finish_day', 'school', 'category', 'dday'))
            return JsonResponse({'check':True, 'data': result}, status=status.HTTP_200_OK)

    return JsonResponse({'check':True, 'data': []}, status=status.HTTP_200_OK)

class EventDetailsView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, event_id, format=None):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventSerializer(event)
        user_has_permission = IsOwnerOrReadOnly().has_object_permission(request, None, event)
        
        response_data = {
            "data": serializer.data,
            "permission": user_has_permission
        }
        
        return Response(response_data, status=status.HTTP_200_OK)




