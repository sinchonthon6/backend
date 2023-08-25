from django.contrib import admin
from django.urls import path
from .views import *

app_name='events'      

urlpatterns = [
    path('', EventCreateAPIView.as_view(), name='create-event')

]