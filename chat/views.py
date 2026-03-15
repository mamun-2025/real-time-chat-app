from django.shortcuts import render

def chat_view(request):
   return render(request, 'chat/chat_room.html') 

# Create your views here.
