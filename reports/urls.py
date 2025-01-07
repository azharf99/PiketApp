from django.urls import path
from reports.views import ReportListView, ReportDetailView, ReportCreateView, ReportUpdateView, ReportDeleteView

urlpatterns = [
    path('', ReportListView.as_view(),  {"site_title": "REPORT LIST - PIKET SMA IT AL BINAA"}, "report-list"),
    path("create/", ReportCreateView.as_view(),  {"site_title": "CREATE REPORT - PIKET SMA IT AL BINAA"}, "report-create"),
    path("detail/<int:pk>/", ReportDetailView.as_view(),  {"site_title": "REPORT DETAIL - PIKET SMA IT AL BINAA"}, "report-detail"),
    path("update/<int:pk>/", ReportUpdateView.as_view(),  {"site_title": "UPDATE REPORT - PIKET SMA IT AL BINAA"}, "report-update"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(),  {"site_title": "DELETE REPORT - PIKET SMA IT AL BINAA"}, "report-delete"),
]
