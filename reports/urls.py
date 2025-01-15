from django.urls import path
from reports.views import ReportListView, ReportDetailView, ReportDeleteView, \
                         ReportDownloadExcelView, ReportUploadView, ReportQuickCreateViewV2, ReportUpdateViewV2
from reports.legacy_views import ReportUpdateView

urlpatterns = [
    path('', ReportListView.as_view(),  {"site_title": "REPORT LIST - PIKET SMA IT AL BINAA"}, "report-list"),
    path("download/", ReportDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-download"),
    path("quick-create-v2/", ReportQuickCreateViewV2.as_view(),  {"site_title": "QUICK CREATE REPORT V2 - PIKET SMA IT AL BINAA"}, "report-quick-create-v2"),
    path("upload/", ReportUploadView.as_view(),  {"site_title": "UPLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-upload"),
    path("update/<int:pk>/", ReportUpdateView.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update"),
    path("detail/<int:pk>/", ReportDetailView.as_view(),  {"site_title": "REPORT DETAIL - PIKET SMA IT AL BINAA"}, "report-detail"),
    path("update-v2/<int:pk>/", ReportUpdateViewV2.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update-v2"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(),  {"site_title": "DELETE REPORT - PIKET SMA IT AL BINAA"}, "report-delete"),
]
