from django.db.models.query import QuerySet
from classes.models import Class
from datetime import datetime, date
from django.forms import BaseModelForm
from django.http import HttpResponse, Http404
from django.views.generic import CreateView, UpdateView, DetailView
from reports.forms import ReportForm, ReportFormV2
from reports.models import Report
from typing import Any
from django.urls import reverse_lazy
from schedules.models import Schedule
from userlogs.models import UserLog
from utils.mixins import BaseFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseModelView, BaseModelListView, ModelDownloadExcelView
from utils.validate_datetime import validate_date, get_day, parse_to_date
# Create your views here.
    
class ReportListView(BaseModelView, BaseModelDateBasedListView):
    model = Report
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False
    paginate_by = 30

class ReportDetailView(BaseModelView, DetailView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'


class ReportQuickCreateViewV2(BaseFormView, CreateView):
    model = Report
    menu_name = 'report'
    form_class = ReportForm
    template_name = 'reports/report_quick_form-v2.html'
    permission_required = 'reports.add_report'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"
    success_url = reverse_lazy("report-list")

    def create_report_objects(self, valid_query_date: Any, schedule_time: Any) -> bool:
        # Cari data jadwal di hari sesuai query dan di waktu jam 1 sampai  9
        schedule_list = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class") \
                                .filter(schedule_day=get_day(valid_query_date), schedule_time=schedule_time)
        # Jika tidak ditemukan, maka nilai False
        if not schedule_list.exists(): return False
        # Jika ditemukan, maka buat laporan dengan jadwal dimasukkan satu per satu
        for schedule in schedule_list:
            obj, is_created = Report.objects.get_or_create(
                report_date = valid_query_date,
                schedule = schedule,
                defaults={
                    'status': "Hadir"
                }
            )
            print(obj, is_created)
        return True

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_date = self.request.GET.get('query_date', datetime.now().date())
        valid_date = parse_to_date(query_date)
        # Jika ada query date, maka 
        if query_date:
            # Buat variabel untuk menyimpan data gabungan laporan jam 1 - 9
            grouped_data = []
            # Mulai perulangan dari Jam 1 sampai Jam 9
            for i in range(1, 10):
                # Cari apakah ada data laporan pada tanggal/hari sesuai query dari jam 1 sampai 9
                data = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter")\
                            .filter(report_date=valid_date, schedule__schedule_time=i).order_by()
                # Jika ada, maka
                if data.exists():
                    # Masukan datanya ke variabel grouped_data
                    grouped_data.append(data)
                # Jika data tidak ada dan tanggal query lebih atau sama dengan hari ini, maka
                elif valid_date >= datetime.now().date():
                    # Buat data laporan baru dari jam 1 sampai jam 9
                    # Jika ada jadwal yang dipilih untuk laporan kosong, maka tampilkan No data
                    if not self.create_report_objects(valid_date, i): grouped_data.append([{"id": f"{i}{j}", "status": "No data"} for j in range(15)])
                # Jika data tidak ada dan tanggal query kurang dari dari hari ini, maka
                else:
                    # Tampilkan no data
                    grouped_data.append([{"id": f"{i}{j}", "status": "No data"} for j in range(15)])
            context["class"] = Class.objects.all()
            context["grouped_data"] = grouped_data
            context["query_date"] = query_date
        return context



class ReportUpdateViewV2(BaseFormView, UpdateView):
    model = Report
    menu_name = 'report'
    form_class = ReportFormV2
    permission_required = 'reports.change_report'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"
    success_url = reverse_lazy("report-quick-create-v2")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        object = self.get_object()
        reporter = form.cleaned_data["reporter"]
        if reporter:
            reporter = reporter.first_name
        UserLog.objects.create(
            user = reporter or self.request.user.first_name,
            action_flag = "mengubah",
            app = "QUICK REPORT V2",
            message = f"laporan piket {object.report_day} {object.report_date} Jam ke-{object.schedule.schedule_time} {object.schedule.schedule_course} dengan status {form.cleaned_data['status']}",
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context

class ReportDeleteView(BaseModelDeleteView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.delete_report'
    success_url = reverse_lazy("report-list")


class ReportUploadView(BaseModelUploadView):
    template_name = 'reports/report_form.html'
    menu_name = "report"
    permission_required = 'reports.create_report'
    success_url = reverse_lazy("report-list")
    model_class = Report


class ReportDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name = 'reports/download.html'
    header_names = ['No', 'TANGGAL', 'HARI', 'STATUS', 'JAM KE-', 'KELAS', 'PELAJARAN', 'PENGAJAR', 'GURU PENGGANTI', "PETUGAS PIKET"]
    filename = 'LAPORAN PIKET SMA IT Al Binaa.xlsx'
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()