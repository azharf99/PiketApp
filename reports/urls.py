from django.urls import path
from reports.views import ReportListView, ReportDetailView, ReportCreateView, ReportUpdateView, ReportDeleteView

urlpatterns = [
    path('', ReportListView.as_view(), {}, "report-list"),
    path("create/", ReportCreateView.as_view(), {}, "report-create"),
    path("detail/<int:pk>/", ReportDetailView.as_view(), {}, "report-detail"),
    path("update/<int:pk>/", ReportUpdateView.as_view(), {}, "report-update"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(), {}, "report-delete"),
]
