from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from models import Schedule
# Create your views here.


class ScheduleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Schedule
    permission_required = 'schedules.view_schedule'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
    

class ScheduleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Schedule
    permission_required = 'schedules.view_schedule'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ScheduleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Schedule
    permission_required = 'schedules.add_schedule'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ScheduleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Schedule
    permission_required = 'schedules.change_schedule'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ScheduleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Schedule
    permission_required = 'schedules.delete_schedule'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
