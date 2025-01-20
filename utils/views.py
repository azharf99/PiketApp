import calendar
from io import BytesIO
from typing import Any
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponse
from classes.models import Class
from courses.models import Course
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime
from schedules.models import Schedule
from reports.models import Report
from userlogs.models import UserLog
from utils.mixins import BaseAuthorizedModelView, BaseModelQueryListView
from utils.constants import WEEKDAYS
from xlsxwriter import Workbook

class DashboardListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    queryset = Report.objects.all()
    template_name = 'dashboard.html'
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Collect and organize data for dashboard context.
        """
        data = super().get_context_data(**kwargs)
        today = datetime.now()
        today_str = str(today.date())
        today_weekday = WEEKDAYS.get(today.weekday())

        # Users
        active_users = User.objects.filter(is_active=True)
        data["sum_of_user"] = active_users
        data["sum_of_user_category"] = active_users.values('is_superuser').annotate(dcount=Count('is_superuser'))

        # Classes
        all_classes = Class.objects.all()
        data["sum_of_class"] = all_classes
        data["sum_of_class_category"] = all_classes.values('category').annotate(dcount=Count('category'))

        # Courses
        courses = Course.objects.exclude(course_code__in=["APE", "LQ1", "TKL"]).select_related("teacher")
        distinct_courses = courses.values("course_name", "category").distinct()
        data["sum_of_course"] = distinct_courses
        data["sum_of_course_syari"] = distinct_courses.filter(category="Syar'i")
        data["sum_of_course_ashri"] = distinct_courses.filter(category="Ashri")

        # Schedules
        all_schedules = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class").all()
        today_schedules = all_schedules.filter(schedule_day=today_weekday)
        data["sum_of_schedule"] = all_schedules
        data["sum_of_schedule_today"] = today_schedules
        data["sum_of_schedule_teacher"] = today_schedules.values('schedule_course__teacher').distinct().count()
        data["sum_of_schedule_teacher_syari"] = today_schedules.filter(schedule_course__category="Syar'i").values('schedule_course__course_name').distinct().count()
        data["sum_of_schedule_teacher_ashri"] = today_schedules.filter(schedule_course__category="Ashri").values('schedule_course__course_name').distinct().count()

        # Reports
        today_reports = self.queryset.filter(report_date=today_str)
        data["sum_of_report_today"] = today_reports
        data["sum_of_report_status"] = self.queryset.values('status').annotate(dcount=Count('status'))
        data["sum_of_report_today_status"] = today_reports.values('status').annotate(dcount=Count('status'))
        data["report_latest"] = self.queryset[:10]

        # Userlogs

        data["userlogs"] = UserLog.objects.all()[:8]
        return data

    
class TeacherRecapListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    template_name = 'teacher-dashboard.html'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year
        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year)\
                             .values('schedule__schedule_course__teacher','schedule__schedule_course__teacher__first_name')\
                             .annotate(
                                 hadir_count=Count('status',  filter=Q(status="Hadir")),
                                 izin_count=Count('status',  filter=Q(status="Izin")),
                                 sakit_count=Count('status',  filter=Q(status="Sakit")),
                                 alpha_count=Count('status',  filter=Q(status="Tanpa Keterangan")),
                                 all_count=Count('status'),
                                 )\
                             .distinct().order_by()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_month"] = self.request.GET.get('query_month') or datetime.now().month
        context["query_year"] = self.request.GET.get('query_year') or datetime.now().year
        
        context["initial_day"] = f'1/{context["query_month"]}/{context["query_year"]}'
        last_day_of_month = calendar.monthrange(int(context["query_year"]), int(context["query_month"]))[1]
        context["last_day"] = f'{last_day_of_month}/{context["query_month"]}/{context["query_year"]}'
        return context
    

class TeacherAbsenceListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    template_name = 'teacher-report-list.html'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year
        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_month"] = self.request.GET.get('query_month') or datetime.now().month
        context["query_year"] = self.request.GET.get('query_year') or datetime.now().year
        context["initial_day"] = f'1/{context["query_month"]}/{context["query_year"]}'
        last_day_of_month = calendar.monthrange(context["query_year"], context["query_month"])[1]
        context["last_day"] = f'{last_day_of_month}/{context["query_month"]}/{context["query_year"]}'
        return context
    

class TeacherRecapDetailView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False
    template_name = 'teacher-report-list.html'

    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year
        teacher_id = self.kwargs.get("teacher_id")
        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_month"] = self.request.GET.get('query_month') or datetime.now().month
        context["query_year"] = self.request.GET.get('query_year') or datetime.now().year
        context["initial_day"] = f'1/{context["query_month"]}/{context["query_year"]}'
        last_day_of_month = calendar.monthrange(context["query_year"], context["query_month"])[1]
        context["last_day"] = f'{last_day_of_month}/{context["query_month"]}/{context["query_year"]}'
        return context


class TeacherRecapDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-dashboard.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year)\
                             .values('schedule__schedule_course__teacher__first_name')\
                             .annotate(
                                 hadir_count=Count('status',  filter=Q(status="Hadir")),
                                 izin_count=Count('status',  filter=Q(status="Izin")),
                                 sakit_count=Count('status',  filter=Q(status="Sakit")),
                                 alpha_count=Count('status',  filter=Q(status="Tanpa Keterangan")),
                                 all_count=Count('status'),
                                 )\
                             .distinct().order_by()
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'GURU', 'HADIR', 'IZIN', 'SAKIT', 'ALPHA', 'PERSENTASE'])
        row = 1
        
        for data in self.get_queryset():
            percentage = "{:.2f}".format(data.get("hadir_count")/data.get("all_count")*100)
            worksheet.write_row(row, 0, [row, data.get("schedule__schedule_course__teacher__first_name"), data.get("hadir_count"), data.get("izin_count"), data.get("sakit_count"), data.get("alpha_count"), f"{percentage}%"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'REKAP KEHADIRAN GURU SMA IT Al Binaa.xlsx')
    

class TeacherAbsenceDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-dashboard.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'TANGGAL', 'GURU', 'KELAS', 'JAM KE', 'STATUS', 'KETERANGAN'])
        row = 1
        
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, str(data.get("report_date")), data.get("schedule__schedule_course__teacher__first_name"), data.get("schedule__schedule_class__short_class_name"), data.get("schedule__schedule_time"), data.get("status")])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'REKAP KETIDAKHADIRAN GURU SMA IT Al Binaa.xlsx')
    

class TeacherAbsenceDetailDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-dashboard.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year
        teacher_id = self.kwargs.get("teacher_id")

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'TANGGAL', 'GURU', 'KELAS', 'JAM KE', 'STATUS', 'KETERANGAN'])
        row = 1
        
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, str(data.get("report_date")), data.get("schedule__schedule_course__teacher__first_name"), data.get("schedule__schedule_class__short_class_name"), data.get("schedule__schedule_time"), data.get("status")])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'DETAIL KETIDAKHADIRAN GURU SMA IT Al Binaa.xlsx')
    


class ReporterRecapListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False
    template_name = 'teacher-dashboard.html'

    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year
        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('-hadir_count')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_month"] = self.request.GET.get('query_month') or datetime.now().month
        context["query_year"] = self.request.GET.get('query_year') or datetime.now().year
        context["reporters"] = True
        context["initial_day"] = f'1/{context["query_month"]}/{context["query_year"]}'
        last_day_of_month = calendar.monthrange(context["query_year"], context["query_month"])[1]
        context["last_day"] = f'{last_day_of_month}/{context["query_month"]}/{context["query_year"]}'
        return context
    


class ReporterRecapDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-dashboard.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('-hadir_count')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'PETUGAS PIKET', 'JUMLAH JAM'])
        row = 1
        
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, data.get("reporter__first_name"), data.get("hadir_count")])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'REKAP KEHADIRAN PIKET SMA IT Al Binaa.xlsx')