# utils/mixins.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import View
from typing import Any
from utils.menu_link import export_menu_link



class BaseModelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Base view for generic model views with shared functionality."""
    raise_exception = True  # Raise PermissionDenied for unauthorized users
    menu_name = ''

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Shared method to enrich context data."""
        data = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("site_title", "").split(" - ")[0].title()
        data.update(self.kwargs)
        data.update({"form_name": model_name})
        data.update(export_menu_link(f"{self.menu_name}"))
        return data


class BaseFormView(BaseModelView):
    """Base view for form-based views like CreateView and UpdateView."""
    success_message: str = "Action completed successfully!"
    error_message: str = "Action failed!"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)
