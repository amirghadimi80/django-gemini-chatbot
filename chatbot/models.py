# chatbot/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class ChatSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=100, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.title} ({self.id})"

    class Meta:
        ordering = ['-created_at']


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)  # True for user message, False for bot response
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "User" if self.is_user else "Bot"
        return f"{self.session.title} - {sender} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp']
