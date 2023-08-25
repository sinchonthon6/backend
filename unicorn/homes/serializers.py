from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from events.models import *
from datetime import date

class EventSerializer(serializers.ModelSerializer):
    dday=serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields=['id','title','img','start_day', 'finish_day', 'school' ,'category','dday']
    def get_dday(self, instance):
        today=date.today()
        d_day = (instance.start_day - today).days
        return d_day