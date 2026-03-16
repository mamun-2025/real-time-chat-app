
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message, PrivateMessage
from django.contrib.auth.models import User
from django.db import models


@login_required
def room_list(request):
   rooms = Room.objects.all()
   users = User.objects.exclude(id=request.user.id)
   return render(request, 'chat/room_list.html', {
      "rooms": rooms,
      "users": users
      })


@login_required
def chat_room(request, room_name):
   room = get_object_or_404(Room, name=room_name)
   messages_list = Message.objects.filter(room=room).order_by('timestamp')

   if request.method == "POST":
      content = request.POST.get('message')

      if content:
         Message.objects.create(
            room=room,
            sender=request.user,
            content=content
         )
      return redirect('chat_room', room_name=room_name)
   
   return render(request, 'chat/chat_room.html', {
      "room": room,
      "chat_messages": messages_list 
   })

@login_required
def private_chat(request, username):
   other_user = get_object_or_404(User, username=username)
   all_users = User.objects.exclude(id=request.user.id)

   messages = PrivateMessage.objects.filter(
      (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
      (models.Q(sender=other_user) & models.Q(receiver=request.user))
   )

   return render(request, 'chat/private_chat.html', {
      'other_user': other_user,
      'chat_messages': messages,
      'users': all_users,
   })