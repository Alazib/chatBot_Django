from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chat'),
    path('enviar-mensaje/', views.chatbot_api, name='enviar_mensaje'),
]
