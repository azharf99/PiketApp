from django.urls import path
from views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), {}, "course-list"),
    path("create/", CourseCreateView.as_view(), {}, "course-create"),
    path("detail/<int:pk>/", CourseDetailView.as_view(), {}, "course-detail"),
    path("update/<int:pk>/", CourseUpdateView.as_view(), {}, "course-update"),
    path("delete/<int:pk>/", CourseDeleteView.as_view(), {}, "course-delete"),
]
