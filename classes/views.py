from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from classes.models import Class
from classes.forms import ClassForm
from typing import Any
# Create your views here.
class BaseClassView(LoginRequiredMixin, PermissionRequiredMixin):
    """Base view for Class views with common functionality."""
    model = Class
    raise_exception = True  # Raise PermissionDenied for unauthorized users

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data.update(self.kwargs)
        data.update({"form_name": self.kwargs["site_title"].split(" - ")[0].title()})
        return data


class ClassListView(BaseClassView, ListView):
    permission_required = 'classes.view_class'


class ClassDetailView(BaseClassView, DetailView):
    permission_required = 'classes.view_class'


class ClassCreateView(BaseClassView, CreateView):
    form_class = ClassForm
    permission_required = 'classes.add_class'


class ClassUpdateView(BaseClassView, UpdateView):
    form_class = ClassForm
    permission_required = 'classes.change_class'


class ClassDeleteView(BaseClassView, DeleteView):
    permission_required = 'classes.delete_class'
