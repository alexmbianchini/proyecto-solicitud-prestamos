from django.db import models

# Create your models here.
class Solicitante(models.Model):
    dni = models.BigIntegerField()
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    genero = models.CharField(max_length=20, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    email = models.EmailField()
    monto = models.DecimalField(max_digits=20, decimal_places=2)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return self.dni + self.nombre + self.apellido