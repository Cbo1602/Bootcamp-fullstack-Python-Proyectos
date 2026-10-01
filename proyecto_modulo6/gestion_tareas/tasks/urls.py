from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.ProyectoListView.as_view(), name='proyecto_lista'),
    path('registro/', views.RegistroView.as_view(), name='registro'),

    path('proyectos/nuevo/', views.ProyectoCreateView.as_view(), name='proyecto_crear'),
    path('proyectos/<int:pk>/', views.ProyectoDetailView.as_view(), name='proyecto_detalle'),
    path('proyectos/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='proyecto_editar'),
    path('proyectos/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='proyecto_eliminar'),

    path('proyectos/<int:proyecto_pk>/tareas/nueva/', views.TareaCreateView.as_view(), name='tarea_crear'),
    path('tareas/<int:pk>/editar/', views.TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/<int:pk>/eliminar/', views.TareaDeleteView.as_view(), name='tarea_eliminar'),
]
