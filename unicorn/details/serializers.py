from rest_framework import serializers
from events.models import Event
from .permissions import IsOwnerOrReadOnly

class Event_Serializer(serializers.ModelSerializer):
    user_has_permission = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_user_has_permission(self, obj):
        request = self.context.get('request')
        if request and hasattr(obj, 'user'):
            return IsOwnerOrReadOnly().has_object_permission(request, None, obj)
        return False
