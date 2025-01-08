"""
URL configuration for PiketApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from utils.menu_link import export_home_kwargs


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), export_home_kwargs("home", "PIKET"), "home"),
    path('menu/', TemplateView.as_view(template_name='menu.html'), export_home_kwargs("menu", "MENU PIKET"), "menu"),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), export_home_kwargs("dashboard", "DASHBOARD PIKET"), "dashboard"),
    path('accounts/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('class/', include('classes.urls')),
    path('course/', include('courses.urls')),
    path('report/', include('reports.urls')),
    path('schedule/', include('schedules.urls')),
]

# if not settings.TESTING:
#     urlpatterns = [
#         *urlpatterns,
#     ] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)