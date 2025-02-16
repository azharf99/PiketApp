from datetime import datetime
from django.forms import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, FormView
from reports.forms import ReportFormV2, SubmitForm
from reports.models import Report
from typing import Any
from django.urls import reverse, reverse_lazy
from schedules.models import ReporterSchedule
from utils.mixins import BaseAuthorizedFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseAuthorizedModelView, ModelDownloadExcelView, BaseModelQueryListView, QuickReportMixin, ReportUpdateQuickViewMixin, ReportUpdateReporterMixin
from utils.validate_datetime import get_day
from utils.whatsapp_albinaa import send_whatsapp_report
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


class SubmitButtonView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = SubmitForm
    template_name = 'reports/report_quick_form-v3.html'
    success_url = reverse_lazy("report-quick-create-v3")
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()
    permission_required = 'reports.add_report'

    def form_valid(self, form: Any) -> HttpResponse:
        report_date = form.cleaned_data['date_string']
        # Filter and order the queryset
        qs = self.queryset.filter(report_date=report_date).exclude(status="Hadir").order_by('schedule__schedule_time', 'schedule__schedule_class')
        reporter_schedule = ReporterSchedule.objects.filter(schedule_day=get_day(report_date))



        total_time = 10
        if get_day("2025-02-16") == "Ahad":
            total_time = 8
        # Initialize the grouped data list
        grouped_data = []

        # Initialize a dictionary to group reports by schedule_time
        grouped_dict = {}

        # Group the reports by schedule_time
        for report in qs:
            schedule_time = int(report.schedule.schedule_time)
            if schedule_time not in grouped_dict:
                grouped_dict[schedule_time] = []
            grouped_dict[schedule_time].append(report)

        # Create the grouped_data list based on the schedule_time
        for time_num in range(1, total_time):  # Assuming schedule_time ranges from 1 to 9
            if time_num in grouped_dict:
                grouped_data.append(grouped_dict[time_num])
            else:
                grouped_data.append([])

        # print(grouped_data)
             

        messages = f'''*[LAPORAN KETIDAKHADIRAN GURU DALAM KBM]*
*TIM PIKET SMAS IT AL BINAA*
Hari: {get_day(report_date)}, {qs.first().report_date if qs.exists() else datetime.now().date().strftime("%d %B %Y")}
Pukul: {datetime.now().time().strftime("%H:%M:%S")} WIB

'''
        for index_outer in range(len(grouped_data)):
            inner_data_length = len(grouped_data[index_outer])
            if inner_data_length > 0:
                messages += f"Jam ke {index_outer+1} ✅\n"
                for data in grouped_data[index_outer]:
                    messages += f'''
KELAS {data.schedule.schedule_class}
{data.schedule.schedule_course}
Keterangan : {data.status}
Pengganti : {data.subtitute_teacher or "-"}
Catatan : {data.notes or "-"}
'''
                    if data == grouped_data[index_outer][-1]:
                            messages += f'\nPetugas Piket: {data.reporter.first_name if data.reporter else "-"}\n'
                            messages += '--------------------------\n\n'
            else:
                messages += f"Jam ke {index_outer+1} LENGKAP✅\n"
                messages += f'Petugas Piket: {reporter_schedule[index_outer].first_name if reporter_schedule[index_outer] else "-"}\n'
                messages += '--------------------------\n\n'

        send_whatsapp_report(messages)
        return super().form_valid(form)
    

class ReportUpdateViewV3(ReportUpdateQuickViewMixin):
    redirect_url = "report-quick-create-v3"
    app_name = "QUICK REPORT V3"
    queryset = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", "reporter").all()
    

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