from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chat'),
    path('enviar-mensaje/', views.chatbot_api, name='enviar_mensaje'),
]
