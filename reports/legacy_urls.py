from django.urls import path
from reports.legacy_views import ReportCreateView, ReportQuickCreateView, ReportUpdateView

urlpatterns = [
    path("create/", ReportCreateView.as_view(),  {"site_title": "CREATE REPORT - PIKET SMA IT AL BINAA"}, "report-create"),
    path("quick-create/", ReportQuickCreateView.as_view(),  {"site_title": "QUICK CREATE REPORT - PIKET SMA IT AL BINAA"}, "report-quick-create"),
    path("update/<int:pk>/", ReportUpdateView.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update"),
]
