from courses.forms import CourseForm
from courses.models import Course
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from utils.mixins import BaseFormView, BaseModelDeleteView, BaseModelUploadView, BaseModelView, BaseModelListView, ModelDownloadExcelView

# Create your views here.
class CourseListView(BaseModelView, BaseModelListView):
    model = Course
    menu_name = 'course'
    queryset = Course.objects.select_related("teacher").all()
    permission_required = 'courses.view_course'
    raise_exception = False


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


class CourseDeleteView(BaseModelDeleteView):
    model = Course
    menu_name = 'course'
    permission_required = 'courses.delete_course'
    success_url = reverse_lazy("course-list")
    

class CourseUploadView(BaseModelUploadView):
    template_name = 'courses/course_form.html'
    menu_name = "course"
    permission_required = 'courses.create_course'
    success_url = reverse_lazy("course-list")
    model_class = Course
    

class CourseDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'course'
    permission_required = 'courses.view_course'
    template_name = 'courses/download.html'
    header_names = ['No', 'NAMA PELAJARAN', 'KODE', 'PENGAJAR']
    filename = 'DATA PELAJARAN SMA IT Al Binaa.xlsx'
    queryset = Course.objects.select_related("teacher").all()