from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from reports.models import Report
from typing import Any
# Create your views here.
class BaseReportView(LoginRequiredMixin, PermissionRequiredMixin):
    """Base view for Report views with common functionality."""
    model = Report
    raise_exception = True  # Raise PermissionDenied for unauthorized users

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data.update(self.kwargs)
        return data


class ReportListView(BaseReportView, ListView):
    permission_required = 'reports.view_report'
    

class ReportDetailView(BaseReportView, DetailView):
    permission_required = 'reports.view_report'


class ReportCreateView(BaseReportView, CreateView):
    fields = '__all__'
    permission_required = 'reports.add_report'


class ReportUpdateView(BaseReportView, UpdateView):
    fields = '__all__'
    permission_required = 'reports.change_report'


class ReportDeleteView(BaseReportView, DeleteView):
    permission_required = 'reports.delete_report'
