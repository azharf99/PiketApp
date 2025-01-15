from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from reports.forms import ReportForm, QuickReportForm
from reports.models import Report
from typing import Any
from schedules.models import Schedule
from utils.mixins import BaseFormView
from utils.validate_datetime import validate_date, validate_time, get_day, parse_to_date




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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        report_date = self.request.GET.get('report_date', datetime.now().date())
        schedule_time = self.request.GET.get('schedule_time', "1")

        date_valid = validate_date(report_date)
        time_valid = validate_time(schedule_time)

        if not (date_valid and time_valid):
            raise BadRequest("Invalid Date and Time")
        
        if isinstance(report_date, date):
            data = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", )\
                        .filter(report_date=report_date, schedule__schedule_time=schedule_time)
        else:
            data = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher", )\
                        .filter(report_date=parse_to_date(report_date), schedule__schedule_time=schedule_time)

        if data.exists():
            context["reports"] = data
        else:
            context["day"] = get_day(report_date)
            context["schedules"] = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class").filter(schedule_day=context["day"], schedule_time=schedule_time)
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