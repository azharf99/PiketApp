from io import BytesIO
from django.contrib import messages
from django.db import IntegrityError
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from reports.forms import ReportForm
from reports.models import Report
from typing import Any
from utils.mixins import BaseFormView, BaseModelUploadView, BaseModelView, BaseModelListView
from xlsxwriter import Workbook
# Create your views here.

class ReportListView(BaseModelView, BaseModelListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False
    

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