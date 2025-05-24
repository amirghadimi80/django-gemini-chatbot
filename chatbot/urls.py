from django.urls import path
from .views import (
    chatbot, register, ajax_chat, user_panel,
    chat_view, create_chat, send_message, login, logout
)

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('user-panel/', user_panel, name='user_panel'),
    path('chat/<int:session_id>/', chat_view, name='chat_view'),
    path('create_chat/', create_chat, name='create_chat'),
    path('send_message/', send_message, name='send_message'),
    path('ajax/chat/', ajax_chat, name='ajax_chat'),
]
