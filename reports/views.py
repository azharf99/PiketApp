from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from classes.models import Class
from datetime import datetime
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.db import IntegrityError
from django.forms import BaseModelForm
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, FormView
from django.urls import reverse_lazy
from reports.forms import ReportForm, QuickReportForm
from reports.models import Report
from typing import Any
from schedules.models import Schedule
from utils.mixins import BaseFormView, BaseModelUploadView, BaseModelView, BaseModelListView
from utils.validate_datetime import validate_date, validate_time, get_day, parse_to_date
from xlsxwriter import Workbook
# Create your views here.

class ReportView(BaseModelView, BaseModelListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        groupped_qs = []
        for i in range(1, 10):
            qs = super().get_queryset().filter(report_date='2025-01-10', schedule__schedule_time=i)\
                        .values('schedule__schedule_class__short_class_name', 
                                'schedule__schedule_course__teacher__first_name', 
                                'status')\
                        .order_by('schedule__schedule_class__short_class_name')
            groupped_qs.append(qs)
        return groupped_qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["class"] = Class.objects.all()
        return context
    
class ReportListView(BaseModelView, BaseModelListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_class = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        query_date = self.request.GET.get('query_date') if self.request.GET.get('query_date') else ''
        query_time = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None

        is_valid_date = validate_date(query_date)

        if is_valid_date and query_class and query_time:
            return Report.objects.filter(report_date=parse_to_date(query_date), schedule__schedule_class__class_name=query_class, schedule__schedule_time=query_time)
        elif is_valid_date and query_time:
            return Report.objects.filter(report_date=parse_to_date(query_date), schedule__schedule_time=query_time)
        elif is_valid_date and query_class:
            return Report.objects.filter(report_date=parse_to_date(query_date), schedule__schedule_time=query_time)
            
        return super().get_queryset()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_class"] = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        context["query_date"] = self.request.GET.get('query_date') if self.request.GET.get('query_date') else datetime.now().date()
        context["query_time"] = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None
        return context

class ReportDetailView(BaseModelView, DetailView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'


class ReportCreateView(BaseFormView, CreateView):
    model = Report
    menu_name = 'report'
    form_class = ReportForm
    permission_required = 'reports.add_report'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"

class ReportQuickCreateView(BaseFormView, FormView):
    menu_name = 'report'
    form_class = QuickReportForm
    template_name = 'reports/report_quick_form.html'
    permission_required = 'reports.add_report'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"
    success_url = reverse_lazy("report-list")

    def get_form_kwargs(self) -> dict[str, Any]:
        k = super().get_form_kwargs()
        k["report_date"] = self.request.GET.get('report_date')
        k["schedule_time"] = self.request.GET.get('schedule_time')
        return k
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        report_date = self.request.GET.get('report_date', datetime.now().date())
        schedule_time = self.request.GET.get('schedule_time', "1")

        date_valid = validate_date(report_date)
        time_valid = validate_time(schedule_time)

        if not (date_valid and time_valid):
            raise BadRequest("Invalid Date and Time")
        
        data = Report.objects.filter(report_date=parse_to_date(report_date), schedule__schedule_time=schedule_time)
        if data.exists():
            context["reports"] = data
        else:
            context["day"] = get_day(report_date)
            context["schedules"] = Schedule.objects.filter(schedule_day=context["day"], schedule_time=schedule_time)
        context["subtitute_teachers"] = User.objects.all()
        return context
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        report_date = form.cleaned_data["report_date"]
        
        context = self.get_context_data()
        if context.get("schedules", False):
            for data in context["schedules"]:
                sub_teacher = get_object_or_404(User, pk=form.data[f"subtitute_teacher{data.id}"]) if form.data[f"subtitute_teacher{data.id}"] else None
                Report.objects.update_or_create(
                    report_date = report_date,
                    schedule = data,
                    defaults={
                        'status': form.data[f"status{data.id}"],
                        'subtitute_teacher': sub_teacher,
                    }
                )
        else:
            for data in context["reports"]:
                sub_teacher = get_object_or_404(User, pk=form.data[f"subtitute_teacher{data.id}"]) if form.data[f"subtitute_teacher{data.id}"] else None
                Report.objects.update_or_create(
                    report_date = report_date,
                    schedule = data.schedule,
                    defaults={
                        'status': form.data[f"status{data.id}"],
                        'subtitute_teacher': sub_teacher,
                    }
                )

        return super().form_valid(form)

class ReportUpdateView(BaseFormView, UpdateView):
    model = Report
    menu_name = 'report'
    form_class = ReportForm
    permission_required = 'reports.change_report'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class ReportDeleteView(BaseModelView, DeleteView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.delete_report'
    success_url = reverse_lazy("report-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)


class ReportUploadView(BaseModelUploadView):
    template_name = 'reports/report_form.html'
    menu_name = "report"
    permission_required = 'reports.create_report'
    success_url = reverse_lazy("report-list")

    
    def form_valid(self, form: Any) -> HttpResponse:
        try:
            self.process_excel_data(Report, form.cleaned_data["file"])
            return super().form_valid(form)
        except IntegrityError as e:
            self.success_message = f"Upload data sudah terbaru! Note: {str(e)}"
            return super().form_valid(form)
        except Exception as e:
            self.error_message = f"Upload data ditolak! Error: {str(e)}"
            return super().form_invalid(form)


class ReportDownloadExcelView(BaseModelView, BaseModelListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name = 'reports/download.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'TANGGAL', 'HARI', 'STATUS', 'JAM KE-', 'KELAS', 'PELAJARAN', 'PENGAJAR', 'GURU PENGGANTI'])
        row = 1
        for data in self.get_queryset():
            subtitue_teacher = f"{data.subtitute_teacher.first_name} {data.subtitute_teacher.last_name}" if data.subtitute_teacher else ""
            worksheet.write_row(row, 0, [row, f"{data.report_date}", f"{data.report_day}", data.status, data.schedule.schedule_time, f"{data.schedule.schedule_class}", f"{data.schedule.schedule_course.course_name}",
                                         f"{data.schedule.schedule_course.teacher.first_name} {data.schedule.schedule_course.teacher.last_name}", subtitue_teacher])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'LAPORAN PIKET SMA IT Al Binaa.xlsx')