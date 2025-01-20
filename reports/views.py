from datetime import datetime
from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView, FormView
from reports.forms import ReportFormV2, ReportUpdatePetugasForm
from reports.models import Report
from typing import Any
from django.urls import reverse, reverse_lazy
from schedules.models import Schedule
from userlogs.models import UserLog
from utils.mixins import BaseAuthorizedFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseAuthorizedModelView, ModelDownloadExcelView, BaseModelQueryListView, QuickReportMixin, ReportUpdateQuickViewMixin, ReportUpdateReporterMixin
from utils.validate_datetime import get_day, parse_to_date
from utils.whatsapp_albinaa import send_whatsapp_action
# Create your views here.
    
class ReportListView(BaseAuthorizedModelView, BaseModelDateBasedListView):
    model = Report
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()
    menu_name = 'report'
    permission_required = 'reports.view_report'
    raise_exception = False
    paginate_by = 105

class ReportDetailView(BaseAuthorizedModelView, DetailView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'


class ReportQuickCreateViewV3(QuickReportMixin):
    model = Report
    menu_name = 'report'
    form_class = ReportFormV2
    template_name = 'reports/report_quick_form-v3.html'
    permission_required = 'reports.add_report'


class ReportUpdateViewV3(ReportUpdateQuickViewMixin):
    redirect_url = "report-quick-create-v3"
    app_name = "QUICK REPORT V3"
    

class ReportUpdatePetugasViewV3(ReportUpdateReporterMixin):
    redirect_url = "report-quick-create-v3"


class ReportDeleteView(BaseModelDeleteView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.delete_report'
    success_url = reverse_lazy("report-list")


class ReportDeleteAllView(BaseAuthorizedFormView, CreateView):
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