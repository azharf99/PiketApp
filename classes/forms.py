from django import forms
from classes.models import Class

class ClassForm(forms.ModelForm):
        
    class Meta:
        model = Class
        fields = '__all__'
        widgets = {
            'class_name': forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'short_class_name': forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }
