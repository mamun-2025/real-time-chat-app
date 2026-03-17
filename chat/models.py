from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
   name = models.CharField(max_length=255, unique=True)
   users = models.ManyToManyField(User, related_name="chat_rooms")
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.name 
   


class Message(models.Model):
   room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
   sender = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField()
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f"{self.sender.username}: {self.content[:30]}"
   



class PrivateMessage(models.Model):
   sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_private_messages')
   receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_private_messages')
   content = models.TextField()
   timestamp = models.DateTimeField(auto_now_add=True)
   is_delivered = models.BooleanField(default=False)
   is_read = models.BooleanField(default=False)
   
   class Meta:
      ordering = ['timestamp']




class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
   is_online = models.BooleanField(default=False)
   last_seen = models.DateTimeField(null=True, blank=True)

   def __str__(self):
      return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"
   
