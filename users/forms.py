from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
        widgets = {
            "username" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class UserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        widgets = {
            "username" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "date_joined" : forms.DateTimeInput(attrs={"type":"datetime-local", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "last_login" : forms.DateTimeInput(attrs={"type":"datetime-local", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "email" : forms.EmailInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "first_name" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "last_name" : forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "groups" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            "user_permissions" : forms.SelectMultiple(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }


class UserPasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,
                   "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2"]