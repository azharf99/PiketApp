from typing import Any
from classes.models import Class
from courses.models import Course
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime
from schedules.models import Schedule
from reports.models import Report
from utils.mixins import BaseModelView, BaseModelListView

class DashboardListView(BaseModelView, BaseModelListView):
    model = Report
    queryset = Report.objects.all()
    menu_name = "report"
    permission_required = 'reports.view_report'
    raise_exception = False

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["sum_of_user"] = User.objects.all()
        data["sum_of_user_category"] = data["sum_of_user"].values('is_superuser').annotate(dcount=Count('is_superuser')).order_by()
        data["sum_of_class"] = Class.objects.all()
        data["sum_of_class_category"] = data["sum_of_class"].values('category').annotate(dcount=Count('category')).order_by()
        data["sum_of_class_putri"] = data["sum_of_class"].filter(category="Putri").count()
        data["sum_of_course"] = Course.objects.all()
        data["sum_of_course_category"] = data["sum_of_course"].values('category').annotate(dcount=Count('category')).order_by()
        data["sum_of_schedule"] = Schedule.objects.all()
        data["sum_of_schedule_today"] = data["sum_of_schedule"].filter(schedule_day=str(datetime.now().weekday()))
        data["sum_of_schedule_teacher"] = data["sum_of_schedule_today"].values('schedule_course__teacher').distinct().count()
        data["sum_of_schedule_teacher_category"] = data["sum_of_schedule_today"].values('schedule_course__category').annotate(dcount=Count('schedule_course__category')).order_by()
        data["sum_of_report_today"] = self.queryset.filter(report_date=str(datetime.now().date()))
        data["sum_of_report_status"] = self.queryset.values('status').annotate(dcount=Count('status')).order_by()
        data["sum_of_report_today_status"] = data["sum_of_report_today"].values('status').annotate(dcount=Count('status')).order_by()
        data["report_latest"] = self.queryset[:10]
        return data

    