from datetime import datetime
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
from utils.whatsapp_albinaa import send_whatsapp_group
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
        schedule_time = form.cleaned_data['time_string']

        reports = self.queryset.filter(report_date=report_date, schedule__schedule_time=schedule_time)
        reports.update(is_submitted=True)
        rep = reports.values_list("status", flat=True)
        if "Sakit" in rep or "Izin" in rep or "Tanpa Keterangan" in rep:
            reports.update(is_complete=False)
        else:
            reports.update(is_complete=True)

        # Filter and order the queryset
        qs = self.queryset.filter(report_date=report_date).order_by('schedule__schedule_time', 'schedule__schedule_class')
        reporter_schedule = ReporterSchedule.objects.filter(schedule_day=get_day(report_date))


        total_time = 10
        if get_day(report_date) == "Ahad":
            total_time = 8

        # Initialize the grouped data list
        grouped_data = []

        # Initialize a dictionary to group reports by schedule_time
        grouped_dict = {}

        # Group the reports by schedule_time
        for report in qs:
            schedule_time = int(report.schedule.schedule_time)
            is_complete = report.is_complete
            is_submitted = report.is_submitted
            status = report.status
            if schedule_time not in grouped_dict:
                grouped_dict[schedule_time] = []
            elif not is_complete and status != "Hadir":
                grouped_dict[schedule_time].append(report)
            elif is_complete:
                grouped_dict[schedule_time] = [report]

        # Create the grouped_data list based on the schedule_time
        for time_num in range(1, total_time):  # Assuming schedule_time ranges from 1 to 9
            if time_num in grouped_dict:
                grouped_data.append(grouped_dict[time_num])
            else:
                grouped_data.append([])

        messages = f'''*[LAPORAN KETIDAKHADIRAN GURU DALAM KBM]*
*TIM PIKET SMAS IT AL BINAA*
Hari: {get_day(report_date)}, {qs.first().report_date.strftime("%d %B %Y") if qs.exists() else datetime.now().date().strftime("%d %B %Y")}
Pukul: {datetime.now().time().strftime("%H:%M:%S")} WIB

'''
        for index_outer in range(len(grouped_data)):
            inner_data_length = len(grouped_data[index_outer])
            if inner_data_length > 0:
                for inner_index in range(inner_data_length):
                    if grouped_data[index_outer][inner_index].is_complete:
                        messages += f"Jam ke {index_outer+1} ✅ LENGKAP\n"
                    elif inner_index == 0 and not grouped_data[index_outer][inner_index].is_complete:
                        messages += f"Jam ke {index_outer+1} ✅\n"
                        messages += f'''
KELAS {grouped_data[index_outer][inner_index].schedule.schedule_class}
{grouped_data[index_outer][inner_index].schedule.schedule_course}
Keterangan : {grouped_data[index_outer][inner_index].status}
Pengganti : {grouped_data[index_outer][inner_index].subtitute_teacher.first_name if grouped_data[index_outer][inner_index].subtitute_teacher else "-"}
Catatan : {grouped_data[index_outer][inner_index].notes or "-"}
'''
                        
                    elif inner_index != 0 and not grouped_data[index_outer][inner_index].is_complete:
                        messages += f'''
KELAS {grouped_data[index_outer][inner_index].schedule.schedule_class}
{grouped_data[index_outer][inner_index].schedule.schedule_course}
Keterangan : {grouped_data[index_outer][inner_index].status}
Pengganti : {grouped_data[index_outer][inner_index].subtitute_teacher.first_name if grouped_data[index_outer][inner_index].subtitute_teacher else "-"}
Catatan : {grouped_data[index_outer][inner_index].notes or "-"}
'''
                    if inner_index == inner_data_length-1:
                        messages += f'\nPetugas Piket: {grouped_data[index_outer][inner_index].reporter.first_name if grouped_data[index_outer][inner_index].reporter else "-"}\n'
                        messages += '--------------------------\n\n'
            else:
                messages += f"Jam ke {index_outer+1}\n"

        send_whatsapp_group(messages)
        query_params = f'?query_date={report_date}'
        return HttpResponseRedirect(reverse("report-quick-create-v3") + query_params)
    

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