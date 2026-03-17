
from django.urls import path
from .views import room_list, chat_room, private_chat 


urlpatterns = [
    path('', room_list, name='room_list'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
    path('direct/<str:username>/', private_chat, name='private_chat'),
]
