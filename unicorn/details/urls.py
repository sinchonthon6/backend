from django.contrib import admin
from django.urls import path
from . import views
from .views import *

app_name='details'      

urlpatterns = [
    path('search/', views.search, name='keyword'),
    path('<int:event_id>/', EventDetailsView.as_view(), name='event-details'),
]