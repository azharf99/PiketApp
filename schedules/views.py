from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from schedules.models import Schedule
from typing import Any
from utils.mixins import BaseFormView, BaseModelView

# Create your views here.
class ScheduleListView(BaseModelView, ListView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'
    

class ScheduleDetailView(BaseModelView, DetailView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.view_schedule'


class ScheduleCreateView(BaseFormView, CreateView):
    model = Schedule
    menu_name = 'schedule'
    fields = '__all__'
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class ScheduleUpdateView(BaseFormView, UpdateView):
    model = Schedule
    menu_name = 'schedule'
    fields = '__all__'
    permission_required = 'schedules.change_schedule'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class ScheduleDeleteView(BaseModelView, DeleteView):
    model = Schedule
    menu_name = 'schedule'
    permission_required = 'schedules.delete_schedule'
    success_url = reverse_lazy("class-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)
