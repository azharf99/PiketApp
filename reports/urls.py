from django.urls import path
from reports.views import ReportListView, ReportDetailView, ReportCreateView, ReportUpdateView, ReportDeleteView,\
                         ReportDownloadExcelView, ReportUploadView, ReportQuickCreateView, ReportQuickCreateViewV2, ReportView

urlpatterns = [
    path('', ReportListView.as_view(),  {"site_title": "REPORT LIST - PIKET SMA IT AL BINAA"}, "report-list"),
    path("create/", ReportCreateView.as_view(),  {"site_title": "CREATE REPORT - PIKET SMA IT AL BINAA"}, "report-create"),
    path("download/", ReportDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-download"),
    path("quick-create/", ReportQuickCreateView.as_view(),  {"site_title": "QUICK CREATE REPORT - PIKET SMA IT AL BINAA"}, "report-quick-create"),
    path("quick-create-v2/", ReportQuickCreateViewV2.as_view(),  {"site_title": "QUICK CREATE REPORT V2 - PIKET SMA IT AL BINAA"}, "report-quick-create-v2"),
    path("upload/", ReportUploadView.as_view(),  {"site_title": "UPLOAD REPORT - PIKET SMA IT AL BINAA"}, "report-upload"),
    path('view/', ReportView.as_view(template_name='reports/report_view.html'),  {"site_title": "REPORT VIEW - PIKET SMA IT AL BINAA"}, "report-view"),
    path("detail/<int:pk>/", ReportDetailView.as_view(),  {"site_title": "REPORT DETAIL - PIKET SMA IT AL BINAA"}, "report-detail"),
    path("update/<int:pk>/", ReportUpdateView.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(),  {"site_title": "DELETE REPORT - PIKET SMA IT AL BINAA"}, "report-delete"),
]
