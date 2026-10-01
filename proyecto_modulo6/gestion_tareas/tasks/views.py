from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .forms import ProyectoForm, RegistroForm, TareaForm
from .models import Proyecto, Tarea


class RegistroView(FormView):
    """Alta de usuarios usando django.contrib.auth."""

    template_name = 'registration/signup.html'
    form_class = RegistroForm
    success_url = reverse_lazy('tasks:proyecto_lista')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'¡Bienvenido/a, {user.username}!')
        return super().form_valid(form)


class ProyectoListView(LoginRequiredMixin, ListView):
    """Lista únicamente los proyectos del usuario autenticado."""

    model = Proyecto
    template_name = 'tasks/proyecto_lista.html'
    context_object_name = 'proyectos'

    def get_queryset(self):
        return Proyecto.objects.filter(propietario=self.request.user)


class ProyectoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Detalle de un proyecto y sus tareas. Solo accesible por su propietario."""

    model = Proyecto
    template_name = 'tasks/proyecto_detalle.html'
    context_object_name = 'proyecto'

    def test_func(self):
        return self.get_object().propietario == self.request.user


class ProyectoCreateView(LoginRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'tasks/proyecto_form.html'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        messages.success(self.request, 'Proyecto creado correctamente.')
        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'tasks/proyecto_form.html'

    def test_func(self):
        return self.get_object().propietario == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Proyecto actualizado correctamente.')
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proyecto
    template_name = 'tasks/proyecto_confirmar_eliminar.html'
    success_url = reverse_lazy('tasks:proyecto_lista')

    def test_func(self):
        return self.get_object().propietario == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Proyecto eliminado.')
        return super().form_valid(form)


class TareaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tasks/tarea_form.html'

    def test_func(self):
        self.proyecto = get_object_or_404(Proyecto, pk=self.kwargs['proyecto_pk'])
        return self.proyecto.propietario == self.request.user

    def form_valid(self, form):
        form.instance.proyecto = self.proyecto
        messages.success(self.request, 'Tarea agregada correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto'] = self.proyecto
        return context

    def get_success_url(self):
        return self.proyecto.get_absolute_url()


class TareaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tasks/tarea_form.html'

    def test_func(self):
        return self.get_object().proyecto.propietario == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto'] = self.object.proyecto
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Tarea actualizada correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.proyecto.get_absolute_url()


class TareaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tarea
    template_name = 'tasks/tarea_confirmar_eliminar.html'

    def test_func(self):
        return self.get_object().proyecto.propietario == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Tarea eliminada.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.proyecto.get_absolute_url()
