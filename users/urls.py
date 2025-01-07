from django.urls import path
from users.views import MyLoginView, MyLogoutView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView



urlpatterns = [
    path('', UserListView.as_view(),  {"site_title": "USER LIST - PIKET SMA IT AL BINAA"}, "user-list"),
    path('login/', MyLoginView.as_view(),  {"site_title": "USER LOGIN - PIKET SMA IT AL BINAA"}, "login"),
    path('logout/', MyLogoutView.as_view(),  {"site_title": "USER LOGOUT - PIKET SMA IT AL BINAA"}, "logout"),
    path("create/", UserCreateView.as_view(),  {"site_title": "CREATE USER - PIKET SMA IT AL BINAA"}, "user-create"),
    path("detail/<int:pk>/", UserDetailView.as_view(),  {"site_title": "USER DETAIL - PIKET SMA IT AL BINAA"}, "user-detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(),  {"site_title": "UPDATE USER - PIKET SMA IT AL BINAA"}, "user-update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(),  {"site_title": "DELETE USER - PIKET SMA IT AL BINAA"}, "user-delete"),
]