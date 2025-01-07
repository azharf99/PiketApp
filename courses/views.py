from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from courses.models import Course
# Create your views here.


class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'courses.view_course'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
    

class CourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    permission_required = 'courses.view_course'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    fields = '__all__'
    permission_required = 'courses.add_course'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    fields = '__all__'
    permission_required = 'courses.change_course'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    permission_required = 'courses.delete_course'
    raise_exception = True  # Raise PermissionDenied for unauthorized users