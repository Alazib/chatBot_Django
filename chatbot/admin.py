from django.contrib import admin
from django.utils.html import format_html
from .models import Usuario, Conversacion, Mensaje, Estado, Reserva

admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Estado)


@admin.register(Usuario)     #Si registro así una entidad en el admin, puedo personalizar las vistas en el panel del administrador.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_registro',)
    
@admin.register(Reserva) 
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'numero_personas', 'telefono', 'alergias')
    search_fields = ('nombre', 'fecha')
    
    def has_change_permission(self, request, obj=None):
        # Si el usuario no ha solicitado editar, no permite cambios
        if obj is not None and not request.GET.get('edit', False):  # Lógica de bloqueo de edición
            return False
        return super().has_change_permission(request, obj)
    
    def ver_detalles(self, obj):
        # Crear un enlace para la edición de la reserva
        return format_html(
            ''
           '<a href="/admin/chatbot/reserva/{}/change/">✏️ Editar</a>',
            obj.id
        )
    ver_detalles.short_description = 'Detalles'


