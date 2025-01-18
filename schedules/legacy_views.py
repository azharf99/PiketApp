from datetime import datetime
from django.core.exceptions import BadRequest
from django.http import HttpRequest, HttpResponse, JsonResponse
from schedules.forms import ScheduleForm
from schedules.models import Schedule
from typing import Any
from utils.mixins import BaseModelView, BaseModelQueryListView
from utils.validate_datetime import validate_date, validate_time, get_day


# DEPRECATED
class ScheduleAPIView(BaseModelView, BaseModelQueryListView):
    model = Schedule
    menu_name = 'schedule'
    form_class = ScheduleForm
    permission_required = 'schedules.add_schedule'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        date_now = datetime.now().date()
        report_date = request.GET.get('date', str(date_now))
        schedule_time = request.GET.get('time')

        # Validate the provided date and time using WEEKDAYS
        valid_date = validate_date(report_date)
        valid_time = validate_time(schedule_time)

        if not (valid_date and valid_time):
            raise BadRequest("Invalid date or time provided.")

        # Fetch schedules matching the provided date and time
        schedule_qs = Schedule.objects.filter(
            schedule_day=get_day(report_date),
            schedule_time=schedule_time,
        )

        data = {
            "error": not schedule_qs.exists(),
            "data": list(schedule_qs.values()),  # Serialize queryset to JSON
        }
        return JsonResponse(data)