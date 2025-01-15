from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from userlogs.models import UserLog
from userlogs.forms import UserlogForm
from utils.mixins import BaseFormView, BaseModelDeleteView, BaseModelView


# Create your views here.
class UserLogListView(BaseModelView, ListView):
    model = UserLog
    paginate_by = 50
    menu_name = 'userlog'
    permission_required = 'userlogs.add_userlog'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"

class UserLogCreateView(BaseModelView, CreateView):
    model = UserLog
    form_class = UserlogForm
    menu_name = 'userlog'
    permission_required = 'userlogs.add_userlog'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class UserLogDetailView(BaseFormView, DetailView):
    model = UserLog
    menu_name = 'userlog'
    permission_required = 'userlogs.add_userlog'
    success_message = "Input data berhasil!"
    error_message = "Input data ditolak!"


class UserLogUpdateView(BaseFormView, UpdateView):
    model = UserLog
    form_class = UserlogForm
    menu_name = 'userlog'
    permission_required = 'userlogs.add_userlog'
    success_message = "Update data berhasil!"
    error_message = "Update data ditolak!"
    
class UserLogDeleteView(BaseModelDeleteView):
    model = UserLog
    success_url = reverse_lazy("userlog:userlog-index")
    menu_name = 'userlog'
    permission_required = 'userlogs.add_userlog'