from django.contrib import admin

from .models import Proyecto, Tarea


class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 1
    fields = ('titulo', 'prioridad', 'completada', 'fecha_limite')


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'fecha_creacion', 'tareas_pendientes')
    list_filter = ('propietario',)
    search_fields = ('nombre', 'propietario__username')
    date_hierarchy = 'fecha_creacion'
    inlines = [TareaInline]


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'proyecto', 'prioridad', 'completada', 'fecha_limite')
    list_filter = ('completada', 'prioridad', 'proyecto')
    search_fields = ('titulo', 'proyecto__nombre')
    list_editable = ('completada', 'prioridad')
