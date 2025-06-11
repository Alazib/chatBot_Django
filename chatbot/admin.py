from django.contrib import admin
from .models import Usuario, Conversacion, Mensaje, Estado

admin.site.register(Usuario)
admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Estado)
