
from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

urlpatterns = [
   # Jwt authentication endpoints
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   # User Api
   path('users/', api_views.UserListAPI.as_view(), name='api_user_list'),
   path('profile/', api_views.UserProfileAPI.as_view(), name='api_user_profile'),

   # Group/Room Api
   path('rooms/', api_views.RoomListAPI.as_view(), name='api_room_list'),
   path('rooms/<str:room_name>/', api_views.RoomChatAPI.as_view(), name='api_room_chat'),

   # Private Chat APi
   path('messages/private/<str:username>/', api_views.PrivateChatListAPI.as_view(), name="api_private_chat"),
  
   
]

