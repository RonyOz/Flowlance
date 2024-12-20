# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_overview, name='chat_overview'),
    path('room/<int:project_id>/<int:member_id>/', views.chat_room, name='chat_room'),
    path('room/<int:project_id>/<int:member_id>/soft_delete/', views.delete_chat, name='soft_delete_chat'),
    path("upload/", views.upload_message, name="upload_message"),  # Nueva URL para subida de archivos
]
