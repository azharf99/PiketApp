from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from classes.models import Class
# Create your views here.


class ClassListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Class
    permission_required = 'classes.view_class'
    raise_exception = True  # Raise PermissionDenied for unauthorized users
    

class ClassDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Class
    permission_required = 'classes.view_class'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ClassCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Class
    permission_required = 'classes.add_class'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ClassUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Class
    permission_required = 'classes.change_class'
    raise_exception = True  # Raise PermissionDenied for unauthorized users


class ClassDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Class
    permission_required = 'classes.delete_class'
    raise_exception = True  # Raise PermissionDenied for unauthorized users