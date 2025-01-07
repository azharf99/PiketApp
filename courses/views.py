from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from courses.models import Course
from typing import Any
# Create your views here.

class BaseCourseView(LoginRequiredMixin, PermissionRequiredMixin):
    """Base view for Course views with common functionality."""
    model = Course
    raise_exception = True  # Raise PermissionDenied for unauthorized users

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data.update(self.kwargs)
        return data


class CourseListView(BaseCourseView, ListView):
    permission_required = 'courses.view_course'
    

class CourseDetailView(BaseCourseView, DetailView):
    permission_required = 'courses.view_course'


class CourseCreateView(BaseCourseView, CreateView):
    fields = '__all__'
    permission_required = 'courses.add_course'


class CourseUpdateView(BaseCourseView, UpdateView):
    fields = '__all__'
    permission_required = 'courses.change_course'


class CourseDeleteView(BaseCourseView, DeleteView):
    permission_required = 'courses.delete_course'