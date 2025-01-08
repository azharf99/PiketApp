from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from typing import Any
from users.forms import UserForm, UserCreateForm, UserPasswordUpdateForm
from utils.menu_link import export_menu_link


# Create your views here.

class BaseUserView(LoginRequiredMixin, PermissionRequiredMixin):
    """Base view for User views with common functionality."""
    model = User
    raise_exception = True  # Raise PermissionDenied for unauthorized users

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data.update(self.kwargs)
        data.update({"form_name": self.kwargs["site_title"].split(" - ")[0].title()})
        return data


class UserListView(BaseUserView, ListView):
    permission_required = 'users.view_user'
    

class UserDetailView(BaseUserView, DetailView):
    permission_required = 'users.view_user'


class UserCreateView(BaseUserView, CreateView):
    form_class = UserCreateForm
    permission_required = 'users.add_user'
    success_url = reverse_lazy("user-list")



class UserUpdateView(BaseUserView, UpdateView):
    form_class = UserForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy("user-list")



class UserDeleteView(BaseUserView, DeleteView):
    permission_required = 'users.delete_user'
    success_url = reverse_lazy("user-list")



class MyLoginView(LoginView):
    redirect_authenticated_user = True
    
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


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        first_name, last_name = context['object'].first_name, context['object'].last_name
        if first_name or last_name:
            data = "".join([first_name.split(" ")[0][0],last_name.split(" ")[0][0]])
            context['name'] = data
        context.update(export_menu_link("profile"))
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordUpdateForm
    success_url = reverse_lazy("user-change-password-done")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.id == self.kwargs.get("pk") or request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        raise PermissionDenied
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Password Ditolak! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Update Password Berhasil! :)")
        return super().form_valid(form)


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name ="registration/password_change_done.html"