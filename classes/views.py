from classes.models import Class
from classes.forms import ClassForm
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from typing import Any
from utils.mixins import BaseModelView, BaseFormView, BaseModelListView

class ClassListView(BaseModelView, BaseModelListView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.view_class'


class ClassDetailView(BaseModelView, DetailView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.view_class'


class ClassCreateView(BaseFormView, CreateView):
    model = Class
    form_class = ClassForm
    menu_name = "class"
    permission_required = 'classes.add_class'
    success_message = 'Input data berhasil!'
    error_message = 'Input data ditolak!'


class ClassUpdateView(BaseFormView, UpdateView):
    model = Class
    form_class = ClassForm
    menu_name = "class"
    permission_required = 'classes.change_class'
    success_message = 'Update data berhasil!'
    error_message = 'Update data ditolak!'


class ClassDeleteView(BaseModelView, DeleteView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.delete_class'
    success_url = reverse_lazy("class-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Kelas berhasil dihapus!")
        return super().post(request, *args, **kwargs)

