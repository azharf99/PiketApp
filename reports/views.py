from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from reports.forms import ReportForm
from reports.models import Report
from typing import Any
from utils.mixins import BaseFormView, BaseModelView
# Create your views here.

class ReportListView(BaseModelView, ListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    

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
