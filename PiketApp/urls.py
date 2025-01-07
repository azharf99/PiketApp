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
from django.contrib import admin, messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.urls import path, include
from django.views.generic import TemplateView
from typing import Any

class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        if self.request.POST.get("remember"):
            self.request.session.set_expiry(1209600)
        else:
           self.request.session.set_expiry(0)
        return super().form_valid(form)
    
class MyLogoutView(LogoutView):

    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> TemplateResponse:
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), {"site_title": "Piket SMA IT AL BINAA"}, "home"),
    path('accounts/login/', MyLoginView.as_view(), name="login"),
    path('accounts/logout/', MyLogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('class/', include('classes.urls')),
    path('course/', include('courses.urls')),
    path('report/', include('reports.urls')),
    path('schedule/', include('schedules.urls')),
]


urlpatterns += debug_toolbar_urls()