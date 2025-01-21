from classes.models import Class
from classes.forms import ClassForm
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from utils.mixins import BaseModelDeleteView, BaseAuthorizedModelView, BaseAuthorizedFormView, BaseModelQueryListView, BaseModelUploadView, ModelDownloadExcelView

class ClassListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Class
    queryset = Class.objects.all()
    menu_name = "class"
    permission_required = 'classes.view_class'
    raise_exception = False


class ClassDetailView(BaseAuthorizedModelView, DetailView):
    model = Class
    menu_name = "class"
    permission_required = 'classes.view_class'


class ClassCreateView(BaseAuthorizedFormView, CreateView):
    model = Class
    form_class = ClassForm
    menu_name = "class"
    permission_required = 'classes.add_class'


class ClassUpdateView(BaseAuthorizedFormView, UpdateView):
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
    