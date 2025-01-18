from io import BytesIO
from typing import Any
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponse
from classes.models import Class
from courses.models import Course
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime
from schedules.models import Schedule
from reports.models import Report
from userlogs.models import UserLog
from utils.mixins import BaseModelView, BaseModelQueryListView
from utils.constants import WEEKDAYS
from xlsxwriter import Workbook

class DashboardListView(BaseModelView, BaseModelQueryListView):
    model = Report
    queryset = Report.objects.all()
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

        data["userlogs"] = UserLog.objects.all()[:50]
        return data

    
class TeacherDashboardListView(BaseModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month', datetime.now().month) if self.request.GET.get('query_month') else datetime.now().month
        query_year = self.request.GET.get('query_year', datetime.now().year) if self.request.GET.get('query_year') else datetime.now().year

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year)\
                             .values('schedule__schedule_course__teacher__first_name', 'status').annotate(dcount=Count('status')).distinct().order_by('status')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["query_month"] = self.request.GET.get('query_month', datetime.now().month) if self.request.GET.get('query_month') else datetime.now().month
        context["query_year"] = self.request.GET.get('query_year', datetime.now().year) if self.request.GET.get('query_year') else datetime.now().year
        return context
    


class TeacherReportDownloadExcelView(BaseModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name = 'reports/download.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        query_month = self.request.GET.get('query_month') or datetime.now().month
        query_year = self.request.GET.get('query_year') or datetime.now().year

        return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .filter(report_date__month=query_month, report_date__year=query_year)\
                             .values('schedule__schedule_course__teacher__first_name', 'status').annotate(dcount=Count('status')).distinct().order_by('status')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'GURU', 'STATUS', 'JUMLAH JAM'])
        row = 1
        
        for data in self.get_queryset():
            worksheet.write_row(row, 0, [row, data.get("schedule__schedule_course__teacher__first_name"), data.get("status"), data.get("dcount")])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'REKAP KEHADIRAN GURU SMA IT Al Binaa.xlsx')