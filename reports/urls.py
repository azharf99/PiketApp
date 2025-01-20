from django.urls import path
from reports.views import ReportListView, ReportDetailView, ReportDeleteView, ReportDeleteAllView,\
                         ReportDownloadExcelView, ReportUploadView, \
                         ReportQuickCreateViewV3, ReportUpdateViewV3, ReportUpdatePetugasViewV3
from reports.views_version2 import ReportQuickCreateViewV2, ReportUpdateViewV2, ReportUpdatePetugasView
from reports.legacy_views import ReportUpdateView

urlpatterns = [
    path('', ReportListView.as_view(),  {"site_title": "REPORT LIST - PIKET SMA IT AL BINAA"}, "report-list"),
    path("download/", ReportDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-download"),
    path("quick-create-v2/", ReportQuickCreateViewV2.as_view(),  {"site_title": "QUICK CREATE REPORT V2 - PIKET SMA IT AL BINAA"}, "report-quick-create-v2"),
    path("quick-create-v3/", ReportQuickCreateViewV3.as_view(),  {"site_title": "QUICK CREATE REPORT V3 - PIKET SMA IT AL BINAA"}, "report-quick-create-v3"),
    path("upload/", ReportUploadView.as_view(),  {"site_title": "UPLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-upload"),
    path("update/<int:pk>/", ReportUpdateView.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update"),
    path("update/reporter/<str:date>/<int:pk>/", ReportUpdatePetugasView.as_view(),  {"site_title": "UPDATE PETUGAS PIKET - PIKET SMA IT AL BINAA"}, "report-update-reporter"),
    path("update/reporter-v3/<str:date>/<int:pk>/", ReportUpdatePetugasViewV3.as_view(),  {"site_title": "UPDATE PETUGAS PIKET - PIKET SMA IT AL BINAA"}, "report-update-reporter-v3"),
    path("detail/<int:pk>/", ReportDetailView.as_view(),  {"site_title": "REPORT DETAIL - PIKET SMA IT AL BINAA"}, "report-detail"),
    path("update-v2/<int:pk>/", ReportUpdateViewV2.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update-v2"),
    path("update-v3/<int:pk>/", ReportUpdateViewV3.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update-v3"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(),  {"site_title": "DELETE REPORT - PIKET SMA IT AL BINAA"}, "report-delete"),
    path("delete-all/", ReportDeleteAllView.as_view(),  {"site_title": "DELETE REPORT - PIKET SMA IT AL BINAA"}, "report-delete-all"),
]
