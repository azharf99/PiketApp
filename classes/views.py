from typing import Any
from django.http import HttpRequest, HttpResponse
from classes.models import Class
from classes.forms import ClassForm
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from utils.mixins import BaseModelDeleteView, BaseModelView, BaseFormView, BaseModelQueryListView, BaseModelUploadView, ModelDownloadExcelView

class ClassListView(BaseModelView, BaseModelQueryListView):
    model = Class
    queryset = Class.objects.all()
    menu_name = "class"
    permission_required = 'classes.view_class'
    raise_exception = False


class ClassDetailView(BaseModelView, DetailView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.view_class'


class ClassCreateView(BaseFormView, CreateView):
    model = Class
    form_class = ClassForm
    menu_name = "class"
    permission_required = 'classes.add_class'


class ClassUpdateView(BaseFormView, UpdateView):
    model = Class
    form_class = ClassForm
    menu_name = "class"
    permission_required = 'classes.change_class'
    success_message = 'Update data berhasil!'


class ClassDeleteView(BaseModelDeleteView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.delete_class'
    success_url = reverse_lazy("class-list")


class ClassUploadView(BaseModelUploadView):
    template_name = 'classes/class_form.html'
    menu_name = "class"
    permission_required = 'classes.create_class'
    success_url = reverse_lazy("class-list")
    model_class = Class


class ClassDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'class'
    permission_required = 'classes.view_class'
    template_name = 'classes/download.html'
    header_names = ['No', 'NAMA KELAS', 'NAMA SINGKAT']
    filename = 'DATA KELAS SMA IT Al Binaa.xlsx'
    queryset = Class.objects.all()
    