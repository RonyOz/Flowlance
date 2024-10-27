from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_overview, name='chat_overview'),
    path('room/<int:project_id>/<int:member_id>/', views.chat_room, name='chat_room'),

]
