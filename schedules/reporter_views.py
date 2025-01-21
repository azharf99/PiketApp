from datetime import datetime
from django.db.models.query import QuerySet
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from classes.models import Class
from schedules.forms import ReporterScheduleForm, ScheduleForm
from schedules.models import ReporterSchedule
from typing import Any
from utils.mixins import BaseAuthorizedFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseAuthorizedModelView, ModelDownloadExcelView
from utils.constants import WEEKDAYS

# Create your views here.

class ReporterScheduleView(BaseAuthorizedModelView, ListView):
    model = ReporterSchedule
    menu_name = 'reporter-schedule'
    template_name = 'schedules/reporterschedule_view.html'
    queryset = ReporterSchedule.objects.select_related("reporter")
    permission_required = 'schedules.view_reporterschedule'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        groupped_qs = []
        for i in range(1, 10):
            qs = ReporterSchedule.objects.filter(schedule_time=i)\
                        .values('schedule_day', 'schedule_time', 'reporter__first_name')\
                        .order_by()
            if len(qs) > 0:
                groupped_qs.append(qs)
        return groupped_qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["class"] = ['Sabtu', 'Ahad', 'Senin', 'Selasa', 'Rabu', 'Kamis']
        return context
    
    
class ReporterScheduleListView(BaseAuthorizedModelView, BaseModelDateBasedListView):
    model = ReporterSchedule
    queryset = ReporterSchedule.objects.select_related("reporter")
    menu_name = 'reporter-schedule'
    permission_required = 'schedules.view_schedule'
    paginate_by = 50


class ReporterScheduleDetailView(BaseAuthorizedModelView, DetailView):
    model = ReporterSchedule
    menu_name = 'reporter-schedule'
    permission_required = 'schedules.view_schedule'
    raise_exception = False


class ReporterScheduleCreateView(BaseAuthorizedFormView, CreateView):
    model = ReporterSchedule
    menu_name = 'reporter-schedule'
    form_class = ReporterScheduleForm
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class ReporterScheduleUpdateView(BaseAuthorizedFormView, UpdateView):
    model = ReporterSchedule
    menu_name = 'reporter-schedule'
    form_class = ReporterScheduleForm
    permission_required = 'schedules.change_schedule'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class ReporterScheduleDeleteView(BaseModelDeleteView):
    model = ReporterSchedule
    menu_name = 'reporter-schedule'
    permission_required = 'schedules.delete_schedule'
    success_url = reverse_lazy("reporter-schedule-list")


class ReporterScheduleUploadView(BaseModelUploadView):
    template_name = 'schedules/schedule_form.html'
    menu_name = "reporter-schedule"
    permission_required = 'schedules.create_schedule'
    success_url = reverse_lazy("reporter-schedule-list")
    model_class = ReporterSchedule


class ReporterScheduleDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'reporter-schedule'
    permission_required = 'schedules.view_schedule'
    template_name = 'schedules/download.html'
    header_names = ['No', 'HARI', 'JAM KE-', 'PETUGAS PIKET', 'WAKTU MULAI', 'WAKTU AKHIR']
    filename = 'JADWAL GURU PIKET SMA IT Al Binaa.xlsx'
    queryset = ReporterSchedule.objects.select_related("reporter").all()