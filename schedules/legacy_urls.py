from django.urls import path
from schedules.legacy_views import ScheduleAPIView

urlpatterns = [
    path("api/v1/", ScheduleAPIView.as_view(),  {"site_title": "SCHEDULE API - PIKET SMA IT AL BINAA"}, "schedule-api-view"),
]
