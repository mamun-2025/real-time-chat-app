

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from channels.db import database_sync_to_async 
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils import timezone


# Group Chat Consumer for public chat rooms
class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      self.room_name = self.scope['url_route']['kwargs']['room_name']
      self.room_group_name = f'chat_{self.room_name}'

      await self.channel_layer.group_add(
         self.room_group_name,
         self.channel_name
      )
      await self.accept()

   
   async def disconnect(self, code_close):
      await self.channel_layer.group_discard(
         self.room_group_name,
         self.channel_name
      )


   async def receive(self, text_data):
      data = json.loads(text_data)
      message = data['message']
      username = data['username']

      await self.save_message(username, self.room_name, message)

      await self.channel_layer.group_send(
         self.room_group_name,
         {
            'type': 'chat_message',
            'message': message,
            'username': username
         }
      )



   async def chat_message(self, event):
      await self.send(text_data=json.dumps({
         'message': event['message'],
         'username': event['username']
      }))
      

   @database_sync_to_async 
   def save_message(self, username, room_name, message):
      user = User.objects.get(username=username)
      room = Room.objects.get(name=room_name)
      Message.objects.create(sender=user, room=room, content=message)
      

   




# Private Chat Consumer for 1-to-1 chat between users
class PrivateChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      self.me = self.scope['user']

      if self.me.is_anonymous:
         await self.close()
      else:
         self.other_username = self.scope['url_route']['kwargs']['username']
         users = sorted([self.me.username, self.other_username])
         self.room_group_name = f'private_{users[0]}_{users[1]}'

         await self.user_online_status_db(True)

         await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name 
         )

         await self.accept()

         await self.channel_layer.group_send(
            self.room_group_name,
            {
               'type': 'status_broadcast',
               'username': self.me.username,
               'status': 'online'
            }
         )
         


   async def disconnect(self, close_code):

      await self.user_online_status_db(False)

      await self.channel_layer.group_send(
         self.room_group_name,
         {
            'type': 'status_broadcast',
            'username': self.me.username,
            'status': 'offline'
         }
      )
      await self.channel_layer.group_discard(
         self.room_group_name,
         self.channel_name
      )


   # Status Broadcast Send Handler
   async def status_broadcast(self, event):
      await self.send(text_data=json.dumps({
         'type': 'user_online',
         'username': event['username'],
         'status': event['status']
      }))


   # Message Send Handler
   async def chat_message(self, event):
      await self.send(text_data=json.dumps({
         'message': event['message'],
         'sender': event['sender']
      }))


   # Message Receive Handler
   async def receive(self, text_data):
      data = json.loads(text_data)

      # Hadnle Typing Status Send
      if data.get('type') == 'typing_status':
         await self.channel_layer.group_send(
            self.room_group_name,
            {
               'type': 'typing_handler',
               'typing': data['typing'],
               'username': self.me.username 
            }
         )
      elif 'message' in data:
         message = data['message']
         sender = self.me.username 

         await self.save_private_message(message)

         await self.channel_layer.group_send(
            self.room_group_name,
            {
               'type': 'chat_message',
               'message': message,
               'sender': sender
            }
         )

   async def typing_handler(self, event):

      if self.me.username != event['username']:
         await self.send(text_data=json.dumps({
            'type': 'typing_status',
            'typing': event['typing'],
            'username': event['username']
         }))
         





   @database_sync_to_async
   def user_online_status_db(self, is_online):
      profile, created = UserProfile.objects.get_or_create(user=self.me)
      profile.is_online = is_online
      if not is_online:
         profile.last_seen = timezone.now()
      profile.save()
   



   @database_sync_to_async
   def save_private_message(self, message):
      other_user = User.objects.get(username=self.other_username)
      from .models import PrivateMessage
      return PrivateMessage.objects.create(
         sender=self.me,
         receiver=other_user,
         content=message
      )
   
