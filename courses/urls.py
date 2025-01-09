from django.urls import path
from courses.views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView, CourseUploadView, CourseDownloadExcelView

urlpatterns = [
    path('', CourseListView.as_view(), {"site_title": "COURSE LIST - PIKET SMA IT AL BINAA"}, "course-list"),
    path("create/", CourseCreateView.as_view(), {"site_title": "CREATE COURSE - PIKET SMA IT AL BINAA"}, "course-create"),
    path("upload/", CourseUploadView.as_view(), {"site_title": "UPLOAD COURSE - PIKET SMA IT AL BINAA"}, "course-upload"),
    path("download/", CourseDownloadExcelView.as_view(), {"site_title": "DOWNLOAD COURSE - PIKET SMA IT AL BINAA"}, "course-download"),
    path("detail/<int:pk>/", CourseDetailView.as_view(), {"site_title": "COURSE DETAIL - PIKET SMA IT AL BINAA"}, "course-detail"),
    path("update/<int:pk>/", CourseUpdateView.as_view(), {"site_title": "UPDATE COURSE - PIKET SMA IT AL BINAA"}, "course-update"),
    path("delete/<int:pk>/", CourseDeleteView.as_view(), {"site_title": "DELETE COURSE - PIKET SMA IT AL BINAA"}, "course-delete"),
]
