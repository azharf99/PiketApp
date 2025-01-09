from django.db import IntegrityError
from classes.models import Class
from classes.forms import ClassForm
from django.contrib import messages
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from io import BytesIO
from typing import Any
from utils.mixins import BaseModelView, BaseFormView, BaseModelListView, BaseModelUploadView
from xlsxwriter import Workbook

class ClassListView(BaseModelView, BaseModelListView):
    model = Class
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



class ClassUploadView(BaseModelUploadView):
    template_name = 'classes/class_form.html'
    menu_name = "class"
    permission_required = 'classes.create_class'
    success_url = reverse_lazy("class-list")

    
    def form_valid(self, form: Any) -> HttpResponse:
        try:
            self.process_excel_data(Class, form.cleaned_data["file"])
            return super().form_valid(form)
        except IntegrityError as e:
            self.success_message = f"Upload data sudah terbaru! Note: {str(e)}"
            return super().form_valid(form)
        except Exception as e:
            self.error_message = f"Upload data ditolak! Error: {str(e)}"
            return super().form_invalid(form)


class ClassDownloadExcelView(BaseModelView, BaseModelListView):
    model = Class
    menu_name = 'class'
    permission_required = 'classes.view_class'
    template_name = 'classes/download.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'NAMA KELAS', 'NAMA SINGKAT'])
        row = 1
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, f"{data.class_name}", f"{data.short_class_name}"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='DATA KELAS SMA IT Al Binaa.xlsx')