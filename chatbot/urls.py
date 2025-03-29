from django.urls import path
from .views import chatbot

urlpatterns = [
    path('', chatbot, name='chatbot'),  # Root page
    path('chat/', chatbot, name='chatbot'),  # Chat page
]
