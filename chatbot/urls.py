from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chat_view, name='chat'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
]
