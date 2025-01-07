from django.urls import path
from users.views import MyLoginView, MyLogoutView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView



urlpatterns = [
    path('', UserListView.as_view(), {}, "user-list"),
    path('login/', MyLoginView.as_view(), {}, "login"),
    path('logout/', MyLogoutView.as_view(), {}, "logout"),
    path("create/", UserCreateView.as_view(), {}, "user-create"),
    path("detail/<int:pk>/", UserDetailView.as_view(), {}, "user-detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), {}, "user-update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), {}, "user-delete"),
]