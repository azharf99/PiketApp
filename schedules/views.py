from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from schedules.models import Schedule
from typing import Any
from utils.menu_link import export_menu_link

# Create your views here.

class BaseScheduleView(LoginRequiredMixin, PermissionRequiredMixin):
    """Base view for Schedule views with common functionality."""
    model = Schedule
    raise_exception = True  # Raise PermissionDenied for unauthorized users

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        model_name = self.kwargs["site_title"].split(" - ")[0].title()
        data.update(self.kwargs)
        data.update({"form_name": model_name})
        data.update(export_menu_link("schedule"))
        return data

class ScheduleListView(BaseScheduleView, ListView):
    permission_required = 'schedules.view_schedule'
    

class ScheduleDetailView(BaseScheduleView, DetailView):
    permission_required = 'schedules.view_schedule'


class ScheduleCreateView(BaseScheduleView, CreateView):
    fields = '__all__'
    permission_required = 'schedules.add_schedule'


class ScheduleUpdateView(BaseScheduleView, UpdateView):
    fields = '__all__'
    permission_required = 'schedules.change_schedule'


class ScheduleDeleteView(BaseScheduleView, DeleteView):
    permission_required = 'schedules.delete_schedule'
