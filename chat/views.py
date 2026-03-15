
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message


@login_required
def room_list(request):
   rooms = Room.objects.all()
   return render(request, 'chat/room_list.html', {"rooms": rooms})


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