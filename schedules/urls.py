from django.urls import path
from schedules.views import ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView, \
                            ScheduleUploadView, ScheduleDownloadExcelView, ScheduleView
from schedules.reporter_views import ReporterScheduleListView, ReporterScheduleDetailView, ReporterScheduleCreateView, ReporterScheduleUpdateView, ReporterScheduleDeleteView, \
                            ReporterScheduleUploadView, ReporterScheduleDownloadExcelView, ReporterScheduleView

urlpatterns = [
    path('', ScheduleListView.as_view(),  {"site_title": "SCHEDULE LIST - PIKET SMA IT AL BINAA"}, "schedule-list"),
    path("create/", ScheduleCreateView.as_view(),  {"site_title": "CREATE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-create"),
    path('view/', ScheduleView.as_view(),  {"site_title": "SCHEDULE VIEW - PIKET SMA IT AL BINAA"}, "schedule-view"),
    path("upload/", ScheduleUploadView.as_view(),  {"site_title": "UPLOAD SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-upload"),
    path("download/", ScheduleDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-download"),
    path("detail/<int:pk>/", ScheduleDetailView.as_view(),  {"site_title": "SCHEDULE DETAIL - PIKET SMA IT AL BINAA"}, "schedule-detail"),
    path("update/<int:pk>/", ScheduleUpdateView.as_view(),  {"site_title": "UPDATE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-update"),
    path("delete/<int:pk>/", ScheduleDeleteView.as_view(),  {"site_title": "DELETE SCHEDULE - PIKET SMA IT AL BINAA"}, "schedule-delete"),


    
    path('reporter/', ReporterScheduleListView.as_view(),  {"site_title": "JADWAL PIKET LIST - PIKET SMA IT AL BINAA"}, "reporter-schedule-list"),
    path("reporter/create/", ReporterScheduleCreateView.as_view(),  {"site_title": "CREATE JADWAL PIKET - PIKET SMA IT AL BINAA"}, "reporter-schedule-create"),
    path('reporter/view/', ReporterScheduleView.as_view(),  {"site_title": "JADWAL PIKET VIEW - PIKET SMA IT AL BINAA"}, "reporter-schedule-view"),
    path("reporter/upload/", ReporterScheduleUploadView.as_view(),  {"site_title": "UPLOAD JADWAL PIKET - PIKET SMA IT AL BINAA"}, "reporter-schedule-upload"),
    path("reporter/download/", ReporterScheduleDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD JADWAL PIKET - PIKET SMA IT AL BINAA"}, "reporter-schedule-download"),
    path("reporter/detail/<int:pk>/", ReporterScheduleDetailView.as_view(),  {"site_title": "JADWAL PIKET DETAIL - PIKET SMA IT AL BINAA"}, "reporter-schedule-detail"),
    path("reporter/update/<int:pk>/", ReporterScheduleUpdateView.as_view(),  {"site_title": "UPDATE JADWAL PIKET - PIKET SMA IT AL BINAA"}, "reporter-schedule-update"),
    path("reporter/delete/<int:pk>/", ReporterScheduleDeleteView.as_view(),  {"site_title": "DELETE JADWAL PIKET - PIKET SMA IT AL BINAA"}, "reporter-schedule-delete"),
]
