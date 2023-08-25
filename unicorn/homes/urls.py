from django.contrib import admin
from django.urls import path
from .views import *

app_name='homes'      

urlpatterns = [
    path('',HomeView.as_view()),
    path('lists/',EventListView.as_view()),
]