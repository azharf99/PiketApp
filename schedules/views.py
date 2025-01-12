from datetime import datetime, date
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from io import BytesIO
from classes.models import Class
from schedules.forms import ScheduleForm
from schedules.models import Schedule
from typing import Any
from utils.mixins import BaseFormView, BaseModelUploadView, BaseModelView, BaseModelListView
from utils.validate_datetime import parse_to_date, validate_date, validate_time, get_day
from xlsxwriter import Workbook

# Create your views here.

class ScheduleView(BaseModelView, BaseModelListView):
    model = Schedule
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_day = self.request.GET.get('query_day', 'Senin')

        groupped_qs = []
        for i in range(1, 10):
            qs = super().get_queryset().filter(schedule_day=query_day, schedule_time=i)\
                        .values('schedule_class__short_class_name', 
                                'schedule_course__teacher__last_name',
                                'schedule_course__course_code',
                                'schedule_course__course_short_name')\
                        .order_by('schedule_class__short_class_name')
            groupped_qs.append(qs)
        return groupped_qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_type"] = self.request.GET.get('query_type', 'code')
        context["query_day"] = self.request.GET.get('query_day', 'Senin')
        context["class"] = Class.objects.all()
        return context
    
    
class ScheduleListView(BaseModelView, BaseModelListView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        query_class = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        query_day = self.request.GET.get('query_day') if self.request.GET.get('query_time') else None
        query_time = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None

        if query_day and query_class and query_time:
            return Schedule.objects.filter(report_day=query_day, schedule_class__class_name=query_class, schedule_time=query_time)
        elif query_time and query_class:
            return Schedule.objects.filter(schedule_class__class_name=query_class, schedule_time=query_time)
        elif query_class and query_day:
            return Schedule.objects.filter(report_day=query_day, schedule_class__class_name=query_class)
        elif query_day and query_time:
            return Schedule.objects.filter(report_day=query_day, schedule_time=query_time)
        elif query_day:
            return Schedule.objects.filter(report_day=query_day)
        elif query_class:
            return Schedule.objects.filter(schedule_class__class_name=query_class)
        elif query_time:
            return Schedule.objects.filter(schedule_time=query_time)
            
        return super().get_queryset()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_class"] = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        context["query_day"] = self.request.GET.get('query_day') if self.request.GET.get('query_day') else None
        context["query_time"] = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None
        return context
    
class ScheduleAPIView(BaseModelView, BaseModelListView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        date_now = datetime.now().date()
        report_date = request.GET.get('date', str(date_now))
        schedule_time = request.GET.get('time')

        # Validate the provided date and time using WEEKDAYS
        valid_date = validate_date(report_date)
        valid_time = validate_time(schedule_time)

        if not (valid_date and valid_time):
            raise BadRequest("Invalid date or time provided.")

        # Fetch schedules matching the provided date and time
        schedule_qs = Schedule.objects.filter(
            schedule_day=get_day(report_date),
            schedule_time=schedule_time,
        )

        data = {
            "error": not schedule_qs.exists(),
            "data": list(schedule_qs.values()),  # Serialize queryset to JSON
        }
        return JsonResponse(data)

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