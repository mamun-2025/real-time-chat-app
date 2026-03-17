
from rest_framework import serializers
from .models import Room, Message, PrivateMessage, UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
   user = UserSerializer(read_only=True)

   class Meta:
      model = UserProfile
      fields = ['user', 'is_online', 'last_seen']

class MessageSerializer(serializers.ModelSerializer):
   sender = UserSerializer(read_only=True)

   class Meta:
      model = Message
      fields = ['id', 'sender', 'room', 'content', 'timestamp']

class RoomSerializer(serializers.ModelSerializer):
   users = UserSerializer(many=True, read_only=True)

   class Meta:
      model = Room 
      fields = ['id', 'name', 'users', 'created_at']


class PrivateMessageSerializer(serializers.ModelSerializer):
   sender_name = serializers.ReadOnlyField(source='sender.username')
   receiver_name = serializers.ReadOnlyField(source='receiver.username')

   class Meta:
      model = PrivateMessage
      fields = ['id', 'sender', 'sender_name', 'receiver', 'receiver_name', 'content', 'timestamp', 'is_delivered', 'is_read']


      