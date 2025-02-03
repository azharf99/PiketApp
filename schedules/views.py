from datetime import datetime
from django.contrib import messages
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from classes.models import Class
from schedules.forms import ScheduleForm
from schedules.models import Schedule
from typing import Any
from utils.mixins import BaseAuthorizedFormView, BaseModelDateBasedListView, BaseModelDeleteView, BaseModelUploadView, BaseAuthorizedModelView, ModelDownloadExcelView
from utils.constants import WEEKDAYS

# Create your views here.

class ScheduleView(BaseAuthorizedModelView, ListView):
    model = Schedule
    menu_name = 'schedule'
    template_name = 'schedules/schedule_view.html'
    queryset = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class")
    permission_required = 'schedules.view_schedule'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_day = self.request.GET.get('query_day')
        if not query_day:
            query_day = WEEKDAYS.get(datetime.now().weekday())
        groupped_qs = []
        for i in range(1, 10):
            qs = self.queryset.filter(schedule_day=query_day, schedule_time=i)\
                        .values('schedule_class__short_class_name', 
                                'schedule_course__teacher__last_name',
                                'schedule_course__course_code',
                                'schedule_course__course_short_name')\
                        .order_by('schedule_class__short_class_name')
            if qs.exists():
                groupped_qs.append(qs)
            else:
                groupped_qs.append([{"schedule_class__short_class_name": "Kosong", 
                                     "schedule_course__teacher__last_name": "Kosong",
                                     "schedule_course__course_code": "Kosong",
                                     "schedule_course__course_short_name": "Kosong"
                                     } for j in range(15)])
        return groupped_qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_type"] = self.request.GET.get('query_type', 'code')
        if self.request.GET.get('query_day'):
            context["query_day"] = self.request.GET.get('query_day')
        else:
            context["query_day"] = WEEKDAYS.get(datetime.now().weekday())
        context["class"] = Class.objects.all()
        return context
    
    
class ScheduleListView(BaseAuthorizedModelView, BaseModelDateBasedListView):
    model = Schedule
    queryset = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class")
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    paginate_by = 50


class ScheduleSearchView(BaseAuthorizedModelView, BaseModelDateBasedListView):
    model = Schedule
    queryset = Schedule.objects.select_related("schedule_course", "schedule_course__teacher", "schedule_class")
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    template_name = 'schedules/schedule_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        query_class = self.request.GET.get('query_class')
        query_day = self.request.GET.get('query_day')
        query_time = self.request.GET.get('query_time')
        if query_class or query_day or query_time:
            return super().get_queryset()
        else:
            return None

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"search": True})
        return context

class ScheduleDetailView(BaseAuthorizedModelView, DetailView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    raise_exception = False


class ScheduleCreateView(BaseAuthorizedFormView, CreateView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"
    success_url = reverse_lazy("schedule-list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        Schedule.objects.update_or_create(
            schedule_day = form.cleaned_data["schedule_day"],
            schedule_time = form.cleaned_data["schedule_time"],
            schedule_class = form.cleaned_data["schedule_class"],
            defaults=dict(
                schedule_course = form.cleaned_data["schedule_course"],
                time_start = form.data.get("time_start"),
                time_end = form.data.get("time_end"),
            )
        )
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)


class ScheduleUpdateView(BaseAuthorizedFormView, UpdateView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.change_schedule'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class ScheduleDeleteView(BaseModelDeleteView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.delete_schedule'
    success_url = reverse_lazy("schedule-list")


class ScheduleUploadView(BaseModelUploadView):
    template_name = 'schedules/schedule_form.html'
    menu_name = "schedule"
    permission_required = 'schedules.create_schedule'
    success_url = reverse_lazy("schedule-list")
    model_class = Schedule


class ScheduleDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    template_name = 'schedules/download.html'
    header_names = ['No', 'HARI', 'JAM KE-', 'KELAS', 'PELAJARAN', 'PENGAJAR']
    filename = 'DATA JADWAL GURU SMA IT Al Binaa.xlsx'
    queryset = Schedule.objects.select_related("schedule_course", "schedule_course__teacher", "schedule_class").all()