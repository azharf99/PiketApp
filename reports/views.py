from datetime import datetime
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView
from reports.forms import ReportFormV2
from reports.models import Report
from typing import Any
from django.urls import reverse, reverse_lazy
from userlogs.models import UserLog
from utils.mixins import BaseFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseModelView, ModelDownloadExcelView, BaseModelQueryListView, QuickReportMixin
from utils.validate_datetime import parse_to_date
from utils.whatsapp_albinaa import send_whatsapp_action
# Create your views here.
    
class ReportListView(BaseModelView, BaseModelDateBasedListView):
    model = Report
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False
    paginate_by = 105

class ReportDetailView(BaseModelView, DetailView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'


class ReportQuickDashboardView(QuickReportMixin):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name = 'reports/report_quick_form-v2.html'
    
    
class ReportQuickCreateViewV2(QuickReportMixin):
    model = Report
    menu_name = 'report'
    template_name = 'reports/report_quick_form-v2.html'
    permission_required = 'reports.add_report'
    grouped_report_data = []

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.grouped_report_data = []
        query_date = request.GET.get('query_date', datetime.now().date())
        valid_date = parse_to_date(query_date)
        is_now_or_future = False
        # Jika ada query date, maka 
        if query_date:
            # Buat variabel untuk menyimpan data gabungan laporan jam 1 - 9
            class_name = ['10A', '10B', '10C', '10D', '10E', '11A', '11B', '11C', '11D', '11E', '12A', '12B', '12C', '12D', '12E']
            # Mulai perulangan dari Jam 1 sampai Jam 9
            for i in range(1, 10):
                # Cari apakah ada data laporan pada tanggal/hari sesuai query dari jam 1 sampai 9
                data = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter")\
                            .filter(report_date=valid_date, schedule__schedule_time=i).order_by()
                # Jika ada, maka
                if data.exists():
                    if data.count() == 15:
                        # Masukan datanya ke variabel grouped_data
                        self.grouped_report_data.append(data)
                    else:
                        copied_data = [*data]
                        temp_data = self.fill_report_object_gaps(class_name, copied_data, i)
                        self.grouped_report_data.append(temp_data)
                # Jika data tidak ada dan tanggal query lebih atau sama dengan hari ini, maka
                elif valid_date >= datetime.now().date():
                    is_now_or_future = True
                    # Buat data laporan baru dari jam 1 sampai jam 9
                    # Jika ada jadwal yang dipilih untuk laporan kosong, maka tampilkan No data
                    if not self.create_report_objects(valid_date, i): self.grouped_report_data.append([{"id": f"{i}{j}", "status": "No data"} for j in range(15)])
                # Jika data tidak ada dan tanggal query kurang dari dari hari ini, maka
                else:
                    # Tampilkan no data
                    self.grouped_report_data.append([{"id": f"{i}{j}", "status": "No data"} for j in range(15)])
            
            if is_now_or_future:
                param = f"?query_date={query_date}"
                return HttpResponseRedirect(reverse('report-quick-dashboard') + param)
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('report-quick-dashboard'))


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
        status = form.cleaned_data["status"]
        if reporter:
            reporter = reporter.first_name

        message = f"laporan piket {object.report_day} {object.report_date} Jam ke-{object.schedule.schedule_time} {object.schedule.schedule_course} dengan status {status}"
        UserLog.objects.create(
            user = reporter or self.request.user.first_name,
            action_flag = "mengubah",
            app = "QUICK REPORT V2",
            message = message,
        )
        send_whatsapp_action(user=reporter or self.request.user.first_name, action="update", messages=message, type="report/", slug="quick-create-v2/")
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


class ReportDeleteAllView(BaseFormView, CreateView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.delete_report'
    success_url = reverse_lazy("report-list")
    http_method_names = [
        'post'
    ]

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        post_data = request.POST.copy()
        selectAll = post_data.get('selectAll')
        print(selectAll)
        if selectAll == 'on':
            data = post_data.pop("selectAll")
            data = post_data.pop("csrfmiddlewaretoken")
            keys_with_on = [key for key, value in post_data.items() if value == 'on']
            Report.objects.filter(pk__in=keys_with_on).delete()
        return HttpResponseRedirect(reverse('report-list'))
    

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