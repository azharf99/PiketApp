from django.urls import path
from schedules.views import ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView, \
                            ScheduleUploadView, ScheduleDownloadExcelView

urlpatterns = [
    path('', ScheduleListView.as_view(),  {"site_title": "SCHEDULE LIST - PIKET SMA IT AL BINAA"}, "schedule-list"),
    path("create/", ScheduleCreateView.as_view(),  {"site_title": "CREATE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-create"),
    path("upload/", ScheduleUploadView.as_view(),  {"site_title": "UPLOAD SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-upload"),
    path("download/", ScheduleDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-download"),
    path("detail/<int:pk>/", ScheduleDetailView.as_view(),  {"site_title": "SCHEDULE DETAIL - PIKET SMA IT AL BINAA"}, "schedule-detail"),
    path("update/<int:pk>/", ScheduleUpdateView.as_view(),  {"site_title": "UPDATE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-update"),
    path("delete/<int:pk>/", ScheduleDeleteView.as_view(),  {"site_title": "DELETE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-delete"),
]
