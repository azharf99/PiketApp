from django.urls import path
from userlogs.views import UserLogListView, UserLogCreateView, UserLogDetailView, UserLogUpdateView, UserLogDeleteView

urlpatterns = [
    path("", UserLogListView.as_view(), {"site-title": "USERLOG LIST - PIKET SMA IT AL BINAA"}, "userlog-list"),
    path("create/", UserLogCreateView.as_view(), {"site-title": "CREATE USERLOG - PIKET SMA IT AL BINAA"}, "userlog-create"),
    path("detail/<int:pk>/", UserLogDetailView.as_view(), {"site-title": "USERLOG DETAIL - PIKET SMA IT AL BINAA"}, "userlog-detail"),
    path("update/<int:pk>/", UserLogUpdateView.as_view(), {"site-title": "UPDATE USERLOG - PIKET SMA IT AL BINAA"}, "userlog-update"),
    path("delete/<int:pk>/", UserLogDeleteView.as_view(), {"site-title": "DELETE USERLOG - PIKET SMA IT AL BINAA"}, "userlog-delete"),
]