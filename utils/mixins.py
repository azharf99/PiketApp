# utils/mixins.py
from datetime import datetime, date
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.db.models import Q, Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View, ListView, FormView, DeleteView
from pandas import read_excel
from typing import Any
from classes.models import Class
from courses.models import Course
from utils.forms import UploadModelForm
from utils.menu_link import export_menu_link
from xlsxwriter import Workbook
from utils.validate_datetime import parse_to_date, validate_date


# KELAS DEFAULT UNTUK HALAMAN WAJIB LOGIN DAN PERMISSION
class BaseModelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Base view for generic model views with shared functionality."""
    raise_exception = False  # Raise PermissionDenied for unauthorized users
    menu_name = ''

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Shared method to enrich context data."""
        data = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("site_title", "").split(" - ")[0].title()
        data.update(self.kwargs)
        data.update({"form_name": model_name})
        data.update(export_menu_link(f"{self.menu_name}"))
        return data

# KELAS DEFAULT UNTUK HALAMAN FORM CREATE DAN UPDATE
class BaseFormView(BaseModelView):
    """Base view for form-based views like CreateView and UpdateView."""
    success_message: str = "Input data berhasil!"
    error_message: str = "Gagal input. Ada sesuatu yang salah!"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


# KELAS DEFAULT UNTUK HALAMAN FORM DELETE
class BaseModelDeleteView(BaseModelView, DeleteView):
    """Base view for DeleteView."""
    success_message: str = "Data berhasil dihapus!"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().post(request, *args, **kwargs)


# KELAS DEFAULT UNTUK HALAMAN YANG MENGGUNAKAN QUERY DI LISTVIEW
class BaseModelListView(ListView):
    """Base view for generic model views with shared functionality."""
    model = None
    
    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get("query")
        if query:
            match self.model.__qualname__:
                case "Class":
                    queryset = self.model.objects.filter(Q(class_name__icontains=query) | Q(short_class_name__icontains=query))
                    return queryset
                case "Course":
                    queryset = self.model.objects.select_related("teacher").filter(Q(course_name__icontains=query) | Q(course_code__icontains=query) | Q(category__icontains=query) | Q(teacher__first_name__icontains=query))
                    return queryset
                case "User":
                    queryset = self.model.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
                    return queryset
                case _:
                    raise Http404("Model dalam ListView tidak ditemukan!")
        return super().get_queryset()
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('query')
        return context


# KELAS DEFAULT UNTUK HALAMAN YANG MENGGUNAKAN QUERY KOMPLEKS BERTANGGAL DI LISTVIEW
class BaseModelDateBasedListView(ListView):
    """Base view for generic model views with shared functionality."""
    model = None
    
    def get_queryset(self) -> QuerySet[Any]:
        query_class = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        query_day = self.request.GET.get('query_day') if self.request.GET.get('query_day') else None
        query_time = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None
        query_date = self.request.GET.get('query_date')

        valid_date = parse_to_date(query_date)
        
        if query_day and query_class and query_time:
            return self.queryset.filter(schedule_day=query_day, schedule_class__class_name=query_class, schedule_time=query_time)
        elif query_time and query_class:
            match self.model.__qualname__:
                case "Schedule":
                    return self.queryset.filter(schedule_class__class_name=query_class, schedule_time=query_time)
                case "Report":
                    return self.queryset.filter(report_date=valid_date, schedule__schedule_class__class_name=query_class, schedule__schedule_time=query_time)
        elif query_class and query_day:
            return self.queryset.filter(schedule_day=query_day, schedule_class__class_name=query_class)
        elif query_day and query_time:
            return self.queryset.filter(schedule_day=query_day, schedule_time=query_time)
        elif query_day:
            return self.queryset.filter(schedule_day=query_day)
        elif query_class:
            match self.model.__qualname__:
                case "Schedule":
                    return self.queryset.filter(schedule_class__class_name=query_class)
                case "Report":
                    return self.queryset.filter(report_date=valid_date, schedule__schedule_class__class_name=query_class)
        elif query_time:
            match self.model.__qualname__:
                case "Schedule":
                    return self.queryset.filter(schedule_time=query_time)
                case "Report":
                    return self.queryset.filter(report_date=valid_date, schedule__schedule_time=query_time)
            
        return super().get_queryset()
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_class"] = self.request.GET.get('query_class') if self.request.GET.get('query_class') else None
        context["query_date"] = self.request.GET.get('query_date') if self.request.GET.get('query_date') else datetime.now().date()
        context["query_day"] = self.request.GET.get('query_day') if self.request.GET.get('query_day') else None
        context["query_time"] = self.request.GET.get('query_time') if self.request.GET.get('query_time') else None
        return context


# KELAS DEFAULT UNTUK HALAMAN UPLOAD EXCEL KE DATABASE
class BaseModelUploadView(BaseModelView, FormView):
    """Base view for generic model views with shared functionality."""
    form_class = UploadModelForm
    success_message: str = "Upload completed successfully!"
    error_message: str = "Upload failed!"
    model_class = None

    def process_excel_data(self, model_name: Model, file: str):
        """Process the uploaded Excel file and update or create Class instances."""
        df = read_excel(
                file,
                na_filter=False,
            )
        row, _ = df.shape
        for i in range(row):
            match model_name.__qualname__:
                case "Class":
                    model_name.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        class_name = df.iloc[i, 1],
                        defaults={
                            "short_class_name": df.iloc[i, 2],
                            "category": df.iloc[i, 3],
                        },
                    )
                case "Course":
                    teacher = get_object_or_404(User, id=df.iloc[i, 5])
                    model_name.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        # course_name = df.iloc[i, 1],
                        # teacher = teacher,
                        defaults={
                            "course_name": df.iloc[i, 2],
                            "teacher": teacher,
                            "course_short_name": df.iloc[i, 2],
                            "course_code": df.iloc[i, 3],
                            "category": df.iloc[i, 4],
                        },
                    )

                case "Schedule":
                    course = get_object_or_404(Course, id=df.iloc[i, 3])
                    class_name = get_object_or_404(Class, id=df.iloc[i, 4])
                    model_name.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        schedule_day = df.iloc[i, 1],
                        schedule_time = str(df.iloc[i, 2]),
                        defaults={
                            "schedule_course": course,
                            "schedule_class": class_name,
                            "time_start": df.iloc[i, 5],
                            "time_end": df.iloc[i, 6],
                        },
                    )
                case "User":
                    group = get_object_or_404(Group, pk=df.iloc[i, 8])
                    obj, is_created = User.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        username = df.iloc[i, 0],
                        defaults={
                            "first_name": df.iloc[i, 3],
                            "last_name": df.iloc[i, 4],
                            "email": df.iloc[i, 5],
                            "is_staff": True if df.iloc[i, 6] else False,
                            "is_superuser": True if df.iloc[i, 7] else False,
                        },
                    )
                    if is_created:
                        obj.set_password(df.iloc[i, 2])
                        obj.save()
                    obj.groups.add(group)
                case _:
                    print("Error Case!")
                    
    
    def form_valid(self, form: Any) -> HttpResponse:
        try:
            if self.model_class is None: raise Http404("Model tidak ditemukan!")
            self.process_excel_data(self.model_class, form.cleaned_data["file"])
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        except IntegrityError as e:
            self.error_message = f"Upload data sudah terbaru! Note: {str(e)}"
            messages.error(self.request, self.error_message)
            return super().form_invalid(form)
        except Exception as e:
            self.error_message = f"Upload data ditolak! Error: {str(e)}"
            messages.error(self.request, self.error_message)
            return super().form_invalid(form)



class ModelDownloadExcelView(BaseModelView):
    header_names = []
    filename = ''
    queryset = None

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, self.header_names)
        row = 1
        for data in (self.queryset or [{"data": "Error!"}]):
            if self.menu_name == 'class':
                worksheet.write_row(row, 0, [row, f"{data.class_name}", f"{data.short_class_name}"])
            elif self.menu_name == 'course':
                worksheet.write_row(row, 0, [row, f"{data.course_name}", f"{data.course_code}", f"{data.teacher.first_name} {data.teacher.last_name}"])
            elif self.menu_name == 'report':
                subtitute_teacher = f"{data.subtitute_teacher.first_name}" if data.subtitute_teacher else ""
                reporter = f"{data.reporter.first_name}" if data.reporter else ""
                worksheet.write_row(row, 0, [row, f"{data.report_date}", f"{data.report_day}", data.status, data.schedule.schedule_time, f"{data.schedule.schedule_class}", f"{data.schedule.schedule_course.course_name}",
                                         f"{data.schedule.schedule_course.teacher.first_name}", subtitute_teacher, reporter])
            elif self.menu_name == 'schedule':
                worksheet.write_row(row, 0, [row, f"{data.schedule_day}", f"{data.schedule_time}", data.schedule_class.class_name, data.schedule_course.course_name, 
                                         f"{data.schedule_course.teacher.first_name} {data.schedule_course.teacher.last_name}"])
            elif self.menu_name == 'user':
                worksheet.write_row(row, 0, [row, data.username, 'Albinaa2004', data.password, data.email, f"{data.is_staff}", f"{data.is_active}",
                                         f'{data.is_superuser}', f"{data.date_joined}", f"{data.last_login}"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=self.filename)