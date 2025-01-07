from django.urls import path
from schedules.views import ScheduleListView, ScheduleDetailView, ScheduleCreateView, ScheduleUpdateView, ScheduleDeleteView

urlpatterns = [
    path('', ScheduleListView.as_view(), {}, "schedule-list"),
    path("create/", ScheduleCreateView.as_view(), {}, "schedule-create"),
    path("detail/<int:pk>/", ScheduleDetailView.as_view(), {}, "schedule-detail"),
    path("update/<int:pk>/", ScheduleUpdateView.as_view(), {}, "schedule-update"),
    path("delete/<int:pk>/", ScheduleDeleteView.as_view(), {}, "schedule-delete"),
]
