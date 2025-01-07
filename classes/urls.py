from django.urls import path
from classes.views import ClassListView, ClassDetailView, ClassCreateView, ClassUpdateView, ClassDeleteView

urlpatterns = [
    path('', ClassListView.as_view(), {}, "class-list"),
    path("create/", ClassCreateView.as_view(), {}, "class-create"),
    path("detail/<int:pk>/", ClassDetailView.as_view(), {}, "class-detail"),
    path("update/<int:pk>/", ClassUpdateView.as_view(), {}, "class-update"),
    path("delete/<int:pk>/", ClassDeleteView.as_view(), {}, "class-delete"),
]
