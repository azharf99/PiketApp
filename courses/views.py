from courses.forms import CourseForm
from courses.models import Course
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from typing import Any
from utils.mixins import BaseFormView, BaseModelView, BaseModelListView

# Create your views here.
class CourseListView(BaseModelView, BaseModelListView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.view_course'
    

class CourseDetailView(BaseModelView, DetailView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.view_course'


class CourseCreateView(BaseFormView, CreateView):
    model = Course
    form_class = CourseForm
    menu_name = 'course'
    permission_required = 'courses.add_course'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class CourseUpdateView(BaseFormView, UpdateView):
    model = Course
    form_class = CourseForm
    menu_name = 'course'
    permission_required = 'courses.change_course'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"


class CourseDeleteView(BaseModelView, DeleteView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.delete_course'
    success_url = reverse_lazy("course-list")

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, "Pelajaran berhasil dihapus!")
        return super().post(request, *args, **kwargs)