
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from django.db.models import Q 
from .models import User, Room, Message, PrivateMessage, UserProfile
from .serializers import UserSerializer, RoomSerializer, MessageSerializer, PrivateMessageSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404


class UserListAPI(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
      search_query = request.query_params.get('search', '')
      if search_query:
         users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id)
      else:
         users = User.objects.all().exclude(id=request.user.id)

      serializer = UserSerializer(users, many=True)
      return Response(serializer.data)
   

class RoomListAPI(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
      rooms = Room.objects.all()
      serializer = RoomSerializer(rooms, many=True)
      return Response(serializer.data)


class RoomChatAPI(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request, room_name):
      try:
         room = Room.objects.get(name=room_name)
         messages = Message.objects.filter(room=room).order_by('timestamp')
         serializer = MessageSerializer(messages, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
      except Room.DoesNotExist:
         return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
      


class PrivateChatListAPI(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request, username):
      messages = PrivateMessage.objects.filter(
         (Q(sender=request.user) & Q(receiver__username=username)) |
         (Q(sender__username=username) & Q(receiver=request.user))
      ).order_by('timestamp') 
      serializer = PrivateMessageSerializer(messages, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
   


class UserProfileAPI(APIView):
   permission_classes = [IsAuthenticated]

   def get(self, request):
      profile = get_object_or_404(UserProfile, user=request.user)
      serializer = UserProfileSerializer(profile)
      return Response(serializer.data)
   


