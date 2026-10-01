from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Proyecto(models.Model):
    """Un proyecto pertenece a un único usuario y agrupa varias tareas."""

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    propietario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='proyectos'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('tasks:proyecto_detalle', kwargs={'pk': self.pk})

    @property
    def tareas_pendientes(self):
        return self.tareas.filter(completada=False).count()


class Tarea(models.Model):
    """Una tarea siempre pertenece a un proyecto (y, a través de él, a un usuario)."""

    class Prioridad(models.TextChoices):
        BAJA = 'baja', 'Baja'
        MEDIA = 'media', 'Media'
        ALTA = 'alta', 'Alta'

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name='tareas'
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    completada = models.BooleanField(default=False)
    prioridad = models.CharField(
        max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA
    )
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['completada', 'fecha_limite', '-prioridad']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('tasks:proyecto_detalle', kwargs={'pk': self.proyecto_id})
