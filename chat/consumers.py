

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from channels.db import database_sync_to_async 
from django.contrib.auth.models import User


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
         

   
class PrivateChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      self.me = self.scope['user']

      if self.me.is_anonymous:
         await self.close()
      else:
         self.other_username = self.scope['url_route']['kwargs']['username']
         users = sorted([self.me.username, self.other_username])
         self.room_group_name = f'private_{users[0]}_{users[1]}'

         await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
         )
         await self.accept()

   async def disconnect(self, clsoe_code):
      await self.channel_layer.group_discard(
         self.room_group_name,
         self.channel_name
      )

   async def receive(self, text_data):
      data = json.loads(text_data)
      message = data['message']
      sender = data['sender']

      await self.save_private_message(message)

      await self.channel_layer.group_send(
         self.room_group_name,
         {
            'type': 'chat_message',
            'message': message,
            'sender': sender
         }
      )

   async def chat_message(self, event):
      await self.send(text_data=json.dumps({
         'message': event['message'],
         'sender': event['sender']
      }))

   @database_sync_to_async
   def save_private_message(self, message):
      other_user = User.objects.get(username=self.other_username)
      from .models import PrivateMessage
      return PrivateMessage.objects.create(
         sender=self.me,
         receiver=other_user,
         content=message
      )