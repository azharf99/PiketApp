# utils/mixins.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q, Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, FormView
from pandas import read_excel
from typing import Any
from classes.models import Class
from courses.models import Course
from utils.forms import UploadModelForm
from utils.menu_link import export_menu_link



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
                    queryset = self.model.objects.select_related("teacher").filter(Q(course_name__icontains=query) | Q(course_code__icontains=query) | Q(teacher__first_name__icontains=query))
                    return queryset
                case "Schedule":
                    queryset = self.model.objects.select_related("schedule_course", "schedule_class").filter(Q(schedule_day__icontains=query) | Q(schedule_time__icontains=query) | Q(schedule_course__course_name__icontains=query) | Q(schedule_class__class_name__icontains=query))
                    return queryset
                case "Report":
                    queryset = self.model.objects.select_related("schedule", "subtitute_teacher").filter(Q(report_date__icontains=query) | Q(report_day__icontains=query) | Q(schedule__schedule_day__icontains=query) | Q(schedule__schedule_time__icontains=query) | Q(status__icontains=query) | Q(subtitute_teacher__first_name__icontains=query))
                    return queryset
                case "User":
                    queryset = self.model.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query))
                    return queryset
                case _:
                    return super().get_queryset()
        return super().get_queryset()




class BaseModelUploadView(BaseModelView, FormView):
    """Base view for generic model views with shared functionality."""
    form_class = UploadModelForm
    success_message: str = "Upload completed successfully!"
    error_message: str = "Upload failed!"

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
                        defaults={
                            "class_name": df.iloc[i, 1],
                            "short_class_name": df.iloc[i, 2],
                            "category": df.iloc[i, 3],
                        },
                    )
                case "Course":
                    teacher, is_created = User.objects.get_or_create(id=df.iloc[i, 3], defaults={"user_name": f"username{df.iloc[i, 3]}", 
                                                                                        "password1": "Albinaa2004",
                                                                                        "password2": "Albinaa2004",
                                                                                    })
                    model_name.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        course_name = df.iloc[i, 1],
                        teacher_id = teacher,
                        defaults={
                            "course_code": df.iloc[i, 2],
                            "category": df.iloc[i, 4],
                        },
                    )

                case "Schedule":
                    course, is_created = Course.objects.get_or_create(id=str(df.iloc[i, 3]), defaults={"course_name": f'Pelajaran{df.iloc[i, 3]}',
                                                                                        "course_code": f'Pelajaran{df.iloc[i, 3]}',})
                    class_name, is_created = Class.objects.get_or_create(id=str(df.iloc[i, 4]), defaults={"class_name": f'Class{df.iloc[i, 4]}',
                                                                                        "short_class_code": f'Class{df.iloc[i, 4]}',})
                    model_name.objects.update_or_create(
                        pk = df.iloc[i, 0],
                        schedule_day = df.iloc[i, 1],
                        schedule_time = str(df.iloc[i, 2]),
                        defaults={
                            "schedule_course": course,
                            "schedule_class": class_name,
                        },
                    )
                case _:
                    print("error case!")
                    
    
    def form_valid(self, form: Any) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form: Any) -> HttpResponse:
        messages.error(self.request, self.error_message)
        return HttpResponseRedirect(reverse(f"{self.menu_name}-upload"))
