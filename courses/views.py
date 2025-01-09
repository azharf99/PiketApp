from io import BytesIO
from django.db import IntegrityError
from courses.forms import CourseForm
from courses.models import Course
from django.contrib import messages
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from typing import Any
from utils.mixins import BaseFormView, BaseModelUploadView, BaseModelView, BaseModelListView
from xlsxwriter import Workbook

# Create your views here.
class CourseListView(BaseModelView, BaseModelListView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.view_course'
    

class CourseDetailView(BaseModelView, DetailView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.view_course'


class CourseCreateView(BaseFormView, CreateView):
    model = Course
    form_class = CourseForm
    menu_name = 'course'
    permission_required = 'courses.add_course'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class CourseUpdateView(BaseFormView, UpdateView):
    model = Course
    form_class = CourseForm
    menu_name = 'course'
    permission_required = 'courses.change_course'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class CourseDeleteView(BaseModelView, DeleteView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.delete_course'
    success_url = reverse_lazy("course-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Pelajaran berhasil dihapus!")
        return super().post(request, *args, **kwargs)
    

class CourseUploadView(BaseModelUploadView):
    template_name = 'courses/course_form.html'
    menu_name = "course"
    permission_required = 'courses.create_course'
    success_url = reverse_lazy("course-list")

    
    def form_valid(self, form: Any) -> HttpResponse:
        try:
            self.process_excel_data(Course, form.cleaned_data["file"])
            return super().form_valid(form)
        except IntegrityError as e:
            self.success_message = f"Upload data sudah terbaru! Note: {str(e)}"
            return super().form_valid(form)
        except Exception as e:
            self.error_message = f"Upload data ditolak! Error: {str(e)}"
            return super().form_invalid(form)


class CourseDownloadExcelView(BaseModelView, BaseModelListView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.view_course'
    template_name = 'courses/download.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'NAMA PELAJARAN', 'KODE', 'PENGAJAR'])
        row = 1
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, f"{data.course_name}", f"{data.course_code}", f"{data.teacher.first_name} {data.teacher.last_name}"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='DATA PELAJARAN SMA IT Al Binaa.xlsx')