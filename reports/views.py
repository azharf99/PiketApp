from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from reports.models import Report
# Create your views here.


class ReportListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Report
    permission_required = 'reports.view_report'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
    

class ReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Report
    permission_required = 'reports.view_report'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ReportCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Report
    permission_required = 'reports.add_report'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ReportUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Report
    permission_required = 'reports.change_report'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ReportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Report
    permission_required = 'reports.delete_report'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
