from django.urls import path
from users.views import MyLoginView, MyLogoutView, MyProfileView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, \
                        UserPasswordChangeDoneView, UserPasswordChangeView, UserUploadView, UserDownloadExcelView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', UserListView.as_view(),  {"site_title": "USER LIST - PIKET SMA IT AL BINAA"}, "user-list"),
    path('password_change/', UserPasswordChangeView.as_view(), {"site_title": "USER PASSWORD CHANGE - PIKET SMA IT AL BINAA"}, "user-change-password"),
    path('password/done', UserPasswordChangeDoneView.as_view(), {"site_title": "USER PASSWORD CHANGE DONE - PIKET SMA IT AL BINAA"}, "password_change_done"),
    path('login/', MyLoginView.as_view(),  {"site_title": "PIKET USER LOGIN - PIKET SMA IT AL BINAA"}, "login"),
    path('profile/', MyProfileView.as_view(),  {"site_title": "USER PROFILE - PIKET SMA IT AL BINAA"}, "profile"),
    path('logout/', MyLogoutView.as_view(),  {"site_title": "USER LOGOUT - PIKET SMA IT AL BINAA"}, "logout"),
    path("create/", UserCreateView.as_view(),  {"site_title": "CREATE USER - PIKET SMA IT AL BINAA"}, "user-create"),
    path("upload/", UserUploadView.as_view(),  {"site_title": "UPLOAD USER - PIKET SMA IT AL BINAA"}, "user-upload"),
    path("download/", UserDownloadExcelView.as_view(),  {"site_title": "DOWNLOAD USER - PIKET SMA IT AL BINAA"}, "user-download"),
    path("detail/<int:pk>/", UserDetailView.as_view(),  {"site_title": "USER DETAIL - PIKET SMA IT AL BINAA"}, "user-detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(),  {"site_title": "UPDATE USER - PIKET SMA IT AL BINAA"}, "user-update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(),  {"site_title": "DELETE USER - PIKET SMA IT AL BINAA"}, "user-delete"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]