from django.contrib import admin
from .models import Usuario, Conversacion, Mensaje, Estado

admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Estado)

@admin.register(Usuario)     #Si registro así una entidad en el admin, puedo personalizar las vistas en el panel del administrador.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_registro',)
    

