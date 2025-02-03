import calendar
from collections import defaultdict
from io import BytesIO
from typing import Any
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from classes.models import Class
from courses.models import Course
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime
from schedules.models import ReporterSchedule, Schedule
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
    template_name = 'teacher-reporter-recap.html'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                                .filter(report_date__gte=date_start, report_date__lte=date_end)\
                                .values('schedule__schedule_course__teacher','schedule__schedule_course__teacher__first_name')\
                                .annotate(
                                    hadir_count=Count('status',  filter=Q(status="Hadir")),
                                    izin_count=Count('status',  filter=Q(status="Izin")),
                                    sakit_count=Count('status',  filter=Q(status="Sakit")),
                                    alpha_count=Count('status',  filter=Q(status="Tanpa Keterangan")),
                                    all_count=Count('status'),
                                    )\
                                .distinct().order_by()
        else:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                                .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year)\
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
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month
        last_day_of_month = calendar.monthrange(this_year, this_month)[1]

        if date_start and date_end:
            context["date_start"] = datetime.strptime(date_start, "%Y-%m-%d")
            context["date_end"] = datetime.strptime(date_end, "%Y-%m-%d")
        else:
            context["date_start"] = datetime.strptime(f"{this_year}-{this_month}-1", "%Y-%m-%d")
            context["date_end"] = datetime.strptime(f"{this_year}-{this_month}-{last_day_of_month}", "%Y-%m-%d")

        context["date_start_str"] = date_start
        context["date_end_str"] = date_end
        return context
    

class TeacherAbsenceListView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    template_name = 'teacher-reporter-detail.html'
    raise_exception = False

    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")
        
        else:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month
        last_day_of_month = calendar.monthrange(this_year, this_month)[1]

        if date_start and date_end:
            context["date_start"] = datetime.strptime(date_start, "%Y-%m-%d")
            context["date_end"] = datetime.strptime(date_end, "%Y-%m-%d")
        else:
            context["date_start"] = datetime.strptime(f"{this_year}-{this_month}-1", "%Y-%m-%d")
            context["date_end"] = datetime.strptime(f"{this_year}-{this_month}-{last_day_of_month}", "%Y-%m-%d")

        context["date_start_str"] = date_start
        context["date_end_str"] = date_end
        return context
    

class TeacherRecapDetailView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False
    template_name = 'teacher-reporter-detail.html'

    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        teacher_id = self.kwargs.get("teacher_id")
        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")
        
        else:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month
        last_day_of_month = calendar.monthrange(this_year, this_month)[1]

        if date_start and date_end:
            context["date_start"] = datetime.strptime(date_start, "%Y-%m-%d")
            context["date_end"] = datetime.strptime(date_end, "%Y-%m-%d")
        else:
            context["date_start"] = datetime.strptime(f"{this_year}-{this_month}-1", "%Y-%m-%d")
            context["date_end"] = datetime.strptime(f"{this_year}-{this_month}-{last_day_of_month}", "%Y-%m-%d")

        context["date_start_str"] = date_start
        context["date_end_str"] = date_end
        return context


class TeacherRecapDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-reporter-recap.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end)\
                             .values('schedule__schedule_course__teacher__first_name')\
                             .annotate(
                                 hadir_count=Count('status',  filter=Q(status="Hadir")),
                                 izin_count=Count('status',  filter=Q(status="Izin")),
                                 sakit_count=Count('status',  filter=Q(status="Sakit")),
                                 alpha_count=Count('status',  filter=Q(status="Tanpa Keterangan")),
                                 all_count=Count('status'),
                                 )\
                             .distinct().order_by()
        else:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year)\
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
    template_name='teacher-reporter-recap.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")

        else: 
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
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
    template_name='teacher-reporter-recap.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        teacher_id = self.kwargs.get("teacher_id")

        if date_start and date_end:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=date_start, report_date__year=date_end, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
                             .values('report_date','schedule__schedule_course__teacher__first_name', "schedule__schedule_class__short_class_name", "schedule__schedule_time", "status")\
                             .distinct().order_by("-report_date", "schedule__schedule_class__short_class_name", "schedule__schedule_time")
        
        else:
            return super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher", "schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=datetime.now().month, report_date__year=datetime.now().year, schedule__schedule_course__teacher_id=teacher_id, status__in=["Izin", "Sakit", "Tanpa Keterangan"])\
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
    template_name = 'teacher-reporter-recap.html'

    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month

        if date_start and date_end:
            # Create a calendar object for the month
            this_month = datetime.strptime(date_start, "%Y-%m-%d").month
            this_year = datetime.strptime(date_start, "%Y-%m-%d").year
            month_calendar = calendar.monthcalendar(this_year, this_month)
        else:
            month_calendar = calendar.monthcalendar(datetime.now().year, datetime.now().month)

        
        # Count the number of Tuesdays in the month
        # day_count_in_month = {'Senin': 4, 'Selasa': 4, 'Rabu': 5, 'Kamis': 5, 'Jumat': 5, 'Sabtu': 4, 'Ahad': 4}
        day_count_in_month = {}
        for k, v in WEEKDAYS.items():
            day_count_in_month[v] = sum(1 for week in month_calendar if week[k] != 0)
        
        reporters_counts_data = []
        # {'Tri Setyo Mardi Utomo, S.Pd': 26, 'Suharyadi, M. Pd., Gr.': 8, 'Alif Rezky, M.Pd.': 16, 'Muh. Halidi, S.Si.': 8, 'Radivan Tiravi': 27, 'Wawanto, S. Si.': 8, 'Dadan Ridwanuloh, M.Si.': 8, 'Arie Afriansyah, Lc.': 18, 'Agus Setiawan, S.T.': 8, 'Syafiq Muhammad Rwenky, B.A.': 10, 'Ahmad Reza Febrianto': 18, 'Aam Hamdani, S.Pd.': 20, 'Rifqi Aqwamuddin, Lc.': 10, 'Hario Sadewo P, S.Pd.': 8, 'Harlan, S. Pd.': 8, 'Firyan Ramdhani, S.Pd.': 8, 'Mohamad Alam Novian, M. Pd.': 8}

        for day_key, value_day_count in day_count_in_month.items():
            data = ReporterSchedule.objects.filter(schedule_day=day_key).exclude(reporter__isnull=True)\
                                            .values("schedule_day", "reporter__first_name")\
                                            .annotate(rcount=Count("reporter__first_name")*value_day_count)\
                                            .distinct().order_by("reporter__first_name")
            # print(data)
            for obj in data:
                reporters_counts_data.append(obj)
        
        # Sort list_of_dict by reporter__first_name
        sorted_reporters_counts_data = sorted(reporters_counts_data, key=lambda x: x['reporter__first_name'])

        # Dictionary to store aggregated counts
        aggregated_counts = defaultdict(int)

        # Sum the rcount for each reporter__first_name
        for item in sorted_reporters_counts_data:
            aggregated_counts[item['reporter__first_name']] += item['rcount']
        
        # Convert back to a list of dicts if needed
        result = [{'reporter__first_name': name, 'total_rcount': count} for name, count in aggregated_counts.items()]

        if date_start and date_end:
            null_reporter = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                      .filter(report_date__gte=date_start, report_date__lte=date_end, reporter__isnull=True)\
                                      .exclude(schedule__in=[241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525])\
                                      .values("report_date", "schedule__schedule_day", "schedule__schedule_time")\
                                      .distinct().order_by()
        else:
            null_reporter = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                      .filter(report_date__month=this_month, report_date__year=this_year, reporter__isnull=True)\
                                      .exclude(schedule__in=[241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525])\
                                      .values("report_date", "schedule__schedule_day", "schedule__schedule_time")\
                                      .distinct().order_by()
        # <QuerySet [{'report_date': datetime.date(2025, 1, 21), 'schedule__schedule_day': 'Selasa', 'schedule__schedule_time': '1'}]>

        absen_group_data = []

        for obj in null_reporter:
            data = ReporterSchedule.objects.filter(schedule_day=obj.get("schedule__schedule_day"), schedule_time=obj.get("schedule__schedule_time"))\
                                            .values("reporter__first_name").annotate(absen_count=Count("reporter__first_name")).order_by()
            for obj in data:
                absen_group_data.append(obj)
            # <QuerySet [<ReporterSchedule: Selasa | Jam ke-1 | radivan_tiravi>]>
        if date_start and date_end:
            data = super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('reporter__first_name')
        else:
            data = super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=this_month, report_date__year=this_year, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('reporter__first_name')
        for index in range(len(data)):
            data[index].update(result[index])
            for i in range(len(absen_group_data)):
                if len(absen_group_data) > 0 and data[index].get("reporter__first_name") == absen_group_data[i].get("reporter__first_name"):
                    data[index].update(absen_group_data[i])
        
        return data
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month
        last_day_of_month = calendar.monthrange(this_year, this_month)[1]

        if date_start and date_end:
            context["date_start"] = datetime.strptime(date_start, "%Y-%m-%d")
            context["date_end"] = datetime.strptime(date_end, "%Y-%m-%d")
        else:
            context["date_start"] = datetime.strptime(f"{this_year}-{this_month}-1", "%Y-%m-%d")
            context["date_end"] = datetime.strptime(f"{this_year}-{this_month}-{last_day_of_month}", "%Y-%m-%d")

        context["date_start_str"] = date_start
        context["date_end_str"] = date_end
        context["reporters"] = True
        return context
    


class ReporterRecapDownloadExcelView(BaseAuthorizedModelView, BaseModelQueryListView):
    model = Report
    menu_name = 'report'
    permission_required = 'reports.view_report'
    template_name='teacher-reporter-recap.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')
        this_year = datetime.now().year
        this_month = datetime.now().month

        if date_start and date_end:
            # Create a calendar object for the month
            this_month = datetime.strptime(date_start, "%Y-%m-%d").month
            this_year = datetime.strptime(date_start, "%Y-%m-%d").year
            month_calendar = calendar.monthcalendar(this_year, this_month)
        else:
            month_calendar = calendar.monthcalendar(datetime.now().year, datetime.now().month)

        
        # Count the number of Tuesdays in the month
        # day_count_in_month = {'Senin': 4, 'Selasa': 4, 'Rabu': 5, 'Kamis': 5, 'Jumat': 5, 'Sabtu': 4, 'Ahad': 4}
        day_count_in_month = {}
        for k, v in WEEKDAYS.items():
            day_count_in_month[v] = sum(1 for week in month_calendar if week[k] != 0)
        
        reporters_counts_data = []
        # {'Tri Setyo Mardi Utomo, S.Pd': 26, 'Suharyadi, M. Pd., Gr.': 8, 'Alif Rezky, M.Pd.': 16, 'Muh. Halidi, S.Si.': 8, 'Radivan Tiravi': 27, 'Wawanto, S. Si.': 8, 'Dadan Ridwanuloh, M.Si.': 8, 'Arie Afriansyah, Lc.': 18, 'Agus Setiawan, S.T.': 8, 'Syafiq Muhammad Rwenky, B.A.': 10, 'Ahmad Reza Febrianto': 18, 'Aam Hamdani, S.Pd.': 20, 'Rifqi Aqwamuddin, Lc.': 10, 'Hario Sadewo P, S.Pd.': 8, 'Harlan, S. Pd.': 8, 'Firyan Ramdhani, S.Pd.': 8, 'Mohamad Alam Novian, M. Pd.': 8}

        for day_key, value_day_count in day_count_in_month.items():
            data = ReporterSchedule.objects.filter(schedule_day=day_key).exclude(reporter__isnull=True)\
                                            .values("schedule_day", "reporter__first_name")\
                                            .annotate(rcount=Count("reporter__first_name")*value_day_count)\
                                            .distinct().order_by("reporter__first_name")
            # print(data)
            for obj in data:
                reporters_counts_data.append(obj)
        
        # Sort list_of_dict by reporter__first_name
        sorted_reporters_counts_data = sorted(reporters_counts_data, key=lambda x: x['reporter__first_name'])

        # Dictionary to store aggregated counts
        aggregated_counts = defaultdict(int)

        # Sum the rcount for each reporter__first_name
        for item in sorted_reporters_counts_data:
            aggregated_counts[item['reporter__first_name']] += item['rcount']
        
        # Convert back to a list of dicts if needed
        result = [{'reporter__first_name': name, 'total_rcount': count} for name, count in aggregated_counts.items()]

        if date_start and date_end:
            null_reporter = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                      .filter(report_date__gte=date_start, report_date__lte=date_end, reporter__isnull=True)\
                                      .exclude(schedule__in=[241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525])\
                                      .values("report_date", "schedule__schedule_day", "schedule__schedule_time")\
                                      .distinct().order_by()
        else:
            null_reporter = Report.objects.select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                                      .filter(report_date__month=this_month, report_date__year=this_year, reporter__isnull=True)\
                                      .exclude(schedule__in=[241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525])\
                                      .values("report_date", "schedule__schedule_day", "schedule__schedule_time")\
                                      .distinct().order_by()
        # <QuerySet [{'report_date': datetime.date(2025, 1, 21), 'schedule__schedule_day': 'Selasa', 'schedule__schedule_time': '1'}]>

        absen_group_data = []

        for obj in null_reporter:
            data = ReporterSchedule.objects.filter(schedule_day=obj.get("schedule__schedule_day"), schedule_time=obj.get("schedule__schedule_time"))\
                                            .values("reporter__first_name").annotate(absen_count=Count("reporter__first_name")).order_by()
            for obj in data:
                absen_group_data.append(obj)
            # <QuerySet [<ReporterSchedule: Selasa | Jam ke-1 | radivan_tiravi>]>
        if date_start and date_end:
            data = super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__gte=date_start, report_date__lte=date_end, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('reporter__first_name')
        else:
            data = super().get_queryset().select_related("schedule__schedule_course", "schedule__schedule_course__teacher","schedule__schedule_class", "subtitute_teacher")\
                             .exclude(schedule__schedule_course__course_code__in=["APE", "TKL"])\
                             .filter(report_date__month=this_month, report_date__year=this_year, reporter__isnull=False)\
                             .values('reporter__first_name')\
                             .annotate(hadir_count=Count('reporter__first_name')/15)\
                             .order_by('reporter__first_name')
        for index in range(len(data)):
            data[index].update(result[index])
            for i in range(len(absen_group_data)):
                if len(absen_group_data) > 0 and data[index].get("reporter__first_name") == absen_group_data[i].get("reporter__first_name"):
                    data[index].update(absen_group_data[i])
        
        return data
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        buffer = BytesIO()
        workbook = Workbook(buffer)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['No', 'PETUGAS PIKET', 'JAM HADIR', 'JAM TIDAK HADIR', 'JUMLAH JAM', 'PERSENTASE'])
        row = 1
        
        for data in self.get_queryset():
            percentage = "{:.2f}".format(data.get("hadir_count")/data.get("total_rcount")*100)
            worksheet.write_row(row, 0, [row, data.get("reporter__first_name"), data.get("hadir_count"), data.get("absen_count"), data.get("total_rcount"), f"{percentage}%"])
            row += 1
        worksheet.autofit()
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'REKAP KEHADIRAN TIM PIKET SMA IT Al Binaa.xlsx')