from io import BytesIO
from django.contrib import messages
from django.db import IntegrityError
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from schedules.forms import ScheduleForm
from schedules.models import Schedule
from typing import Any
from utils.mixins import BaseFormView, BaseModelUploadView, BaseModelView, BaseModelListView
from xlsxwriter import Workbook

# Create your views here.
class ScheduleListView(BaseModelView, BaseModelListView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    

class ScheduleDetailView(BaseModelView, DetailView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    raise_exception = False


class ScheduleCreateView(BaseFormView, CreateView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class ScheduleUpdateView(BaseFormView, UpdateView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.change_schedule'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class ScheduleDeleteView(BaseModelView, DeleteView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.delete_schedule'
    success_url = reverse_lazy("schedule-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)


class ScheduleUploadView(BaseModelUploadView):
    template_name = 'schedules/schedule_form.html'
    menu_name = "schedule"
    permission_required = 'schedules.create_schedule'
    success_url = reverse_lazy("schedule-list")

    
    def form_valid(self, form: Any) -> HttpResponse:
        try:
            self.process_excel_data(Schedule, form.cleaned_data["file"])
            return super().form_valid(form)
        except IntegrityError as e:
            self.success_message = f"Upload data sudah terbaru! Note: {str(e)}"
            return super().form_valid(form)
        except Exception as e:
            self.error_message = f"Upload data ditolak! Error: {str(e)}"
            return super().form_invalid(form)


class ScheduleDownloadExcelView(BaseModelView, BaseModelListView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    template_name = 'schedules/download.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'HARI', 'JAM KE-', 'KELAS', 'PELAJARAN', 'PENGAJAR'])
        row = 1
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, f"{data.schedule_day}", f"{data.schedule_time}", data.schedule_class, data.schedule_course.course_name, 
                                         f"{data.schedule_course.teacher.first_name} {data.schedule_course.teacher.last_name}"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='DATA JADWAL GURU SMA IT Al Binaa.xlsx')