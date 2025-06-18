from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Conversacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='conversaciones')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conversacion {self.usuario.nombre} - {self.fecha_inicio}"
    

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    texto = models.TextField()
    remitente = models.CharField(max_length=10, choices=[('bot', 'Chatbot'), ('usuario', 'Usuario')])
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.remitente} en {self.conversacion}"

class Estado(models.Model):
    conversacion = models.OneToOneField(Conversacion, on_delete=models.CASCADE, related_name='estado')
    estado_actual = models.CharField(max_length=255)
    datos = models.JSONField(null=True, blank=True)  # Para almacenar info adicional en formato JSON

    def __str__(self):
        return f"El estado de Conversacion {self.conversacion} es {self.estado_actual}"
    
    
class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    numero_personas = models.IntegerField()
    alergias = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.nombre} para {self.numero_personas} personas el {self.fecha.strftime('%d/%m/%Y %H:%M')}"



