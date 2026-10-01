from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Proyecto, Tarea


class ProyectoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave12345')
        self.proyecto = Proyecto.objects.create(nombre='Web App', propietario=self.user)

    def test_str_devuelve_nombre(self):
        self.assertEqual(str(self.proyecto), 'Web App')

    def test_propietario_asignado(self):
        self.assertEqual(self.proyecto.propietario, self.user)

    def test_tareas_pendientes_inicial(self):
        self.assertEqual(self.proyecto.tareas_pendientes, 0)


class TareaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave12345')
        self.proyecto = Proyecto.objects.create(nombre='Web App', propietario=self.user)
        self.tarea = Tarea.objects.create(proyecto=self.proyecto, titulo='Diseñar modelos')

    def test_str_devuelve_titulo(self):
        self.assertEqual(str(self.tarea), 'Diseñar modelos')

    def test_no_completada_por_defecto(self):
        self.assertFalse(self.tarea.completada)

    def test_prioridad_por_defecto_media(self):
        self.assertEqual(self.tarea.prioridad, Tarea.Prioridad.MEDIA)

    def test_contador_pendientes_del_proyecto(self):
        self.assertEqual(self.proyecto.tareas_pendientes, 1)


class AccesoYPermisosTest(TestCase):
    """Verifica autenticación, autorización y aislamiento entre usuarios."""

    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave12345')
        self.otro_usuario = User.objects.create_user(username='luis', password='clave12345')
        self.proyecto = Proyecto.objects.create(nombre='Privado', propietario=self.user)

    def test_lista_de_proyectos_requiere_login(self):
        response = self.client.get(reverse('tasks:proyecto_lista'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('tasks:proyecto_lista')}"
        )

    def test_usuario_no_puede_ver_proyecto_ajeno(self):
        self.client.login(username='luis', password='clave12345')
        response = self.client.get(
            reverse('tasks:proyecto_detalle', args=[self.proyecto.pk])
        )
        self.assertEqual(response.status_code, 403)

    def test_propietario_ve_su_proyecto(self):
        self.client.login(username='ana', password='clave12345')
        response = self.client.get(
            reverse('tasks:proyecto_detalle', args=[self.proyecto.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_lista_solo_muestra_proyectos_propios(self):
        Proyecto.objects.create(nombre='De Luis', propietario=self.otro_usuario)
        self.client.login(username='ana', password='clave12345')
        response = self.client.get(reverse('tasks:proyecto_lista'))
        proyectos = list(response.context['proyectos'])
        self.assertEqual(proyectos, [self.proyecto])


class ProyectoCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave12345')
        self.client.login(username='ana', password='clave12345')

    def test_crear_proyecto(self):
        response = self.client.post(
            reverse('tasks:proyecto_crear'),
            {'nombre': 'Nuevo Proyecto', 'descripcion': 'desc'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Proyecto.objects.filter(nombre='Nuevo Proyecto').exists())

    def test_formulario_rechaza_nombre_muy_corto(self):
        response = self.client.post(
            reverse('tasks:proyecto_crear'), {'nombre': 'ab', 'descripcion': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Proyecto.objects.filter(nombre='ab').exists())

    def test_eliminar_proyecto(self):
        proyecto = Proyecto.objects.create(nombre='A borrar', propietario=self.user)
        response = self.client.post(
            reverse('tasks:proyecto_eliminar', args=[proyecto.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Proyecto.objects.filter(pk=proyecto.pk).exists())


class TareaCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='clave12345')
        self.proyecto = Proyecto.objects.create(nombre='Web App', propietario=self.user)
        self.client.login(username='ana', password='clave12345')

    def test_crear_tarea(self):
        response = self.client.post(
            reverse('tasks:tarea_crear', args=[self.proyecto.pk]),
            {
                'titulo': 'Configurar admin',
                'descripcion': '',
                'prioridad': 'alta',
                'completada': False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarea.objects.filter(titulo='Configurar admin').exists())

    def test_marcar_tarea_como_completada(self):
        tarea = Tarea.objects.create(proyecto=self.proyecto, titulo='Tests')
        response = self.client.post(
            reverse('tasks:tarea_editar', args=[tarea.pk]),
            {
                'titulo': tarea.titulo,
                'descripcion': '',
                'prioridad': 'media',
                'completada': True,
            },
        )
        self.assertEqual(response.status_code, 302)
        tarea.refresh_from_db()
        self.assertTrue(tarea.completada)
