from rest_framework import serializers
from events.models import Event
# from .permissions import IsOwnerOrReadOnly


class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



