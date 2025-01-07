from django.urls import path
from classes.views import ClassListView, ClassDetailView, ClassCreateView, ClassUpdateView, ClassDeleteView

urlpatterns = [
    path('', ClassListView.as_view(), {"site_title": "CLASS LIST - PIKET SMA IT AL BINAA"}, "class-list"),
    path("create/", ClassCreateView.as_view(), {"site_title": "CREATE CLASS - PIKET SMA IT AL BINAA"}, "class-create"),
    path("detail/<int:pk>/", ClassDetailView.as_view(), {"site_title": "CLASS DETAIL - PIKET SMA IT AL BINAA"}, "class-detail"),
    path("update/<int:pk>/", ClassUpdateView.as_view(), {"site_title": "UPDATE CLASS - PIKET SMA IT AL BINAA"}, "class-update"),
    path("delete/<int:pk>/", ClassDeleteView.as_view(), {"site_title": "DELETE CLASS - PIKET SMA IT AL BINAA"}, "class-delete"),
]
