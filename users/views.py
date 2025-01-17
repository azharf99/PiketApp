from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.core.handlers.wsgi import WSGIRequest
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from typing import Any
from users.forms import UserForm, UserCreateForm, UserPasswordUpdateForm
from utils.menu_link import export_menu_link
from utils.mixins import BaseFormView, BaseModelDeleteView, BaseModelUploadView, BaseModelView, BaseModelListView, ModelDownloadExcelView


# Create your views here.
class UserListView(BaseModelView, BaseModelListView):
    model = User
    queryset = User.objects.all()
    menu_name = 'user'
    permission_required = 'users.view_user'
        

class UserDetailView(BaseModelView, DetailView):
    model = User
    menu_name = 'user'
    permission_required = 'users.view_user'


class UserCreateView(BaseFormView, CreateView):
    model = User
    menu_name = 'user'
    form_class = UserCreateForm
    permission_required = 'users.add_user'
    success_url = reverse_lazy("user-list")
    success_message = 'Input data berhasil!'
    error_message = 'Input data ditolak!'

class UserUpdateView(BaseFormView, UpdateView):
    model = User
    menu_name = 'user'
    form_class = UserForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy("user-list")
    success_message = 'Update data berhasil!'
    error_message = 'Update data ditolak!'


class UserDeleteView(BaseModelDeleteView):
    model = User
    menu_name = 'user'
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
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['site_title'] = "LOGIN PIKET"
        return context
    
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
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Update Password Ditolak! :( Ada kesalahan input!")
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, "Update Password Berhasil! :)")
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(export_menu_link("profile"))
        return context


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name ="registration/password_change_done.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(export_menu_link("profile"))
        return context


class UserUploadView(BaseModelUploadView):
    template_name = 'auth/user_form.html'
    menu_name = "user"
    permission_required = 'users.create_user'
    success_url = reverse_lazy("user-list")
    model_class = User


class UserDownloadExcelView(ModelDownloadExcelView):
    menu_name = 'user'
    permission_required = 'users.view_user'
    template_name = 'auth/download.html'
    header_names = ['No', 'USERNAME', 'PASSWORD', 'PASSWORD', 'EMAIL', 'IS STAFF', 'IS ACTIVE', 'IS ADMIN', 'TANGGAL GABUNG', 'TERAKHIR LOGIN']
    filename = 'USERS PIKET SMA IT Al Binaa.xlsx'
    queryset = User.objects.all()