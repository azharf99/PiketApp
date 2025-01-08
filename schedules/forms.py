from django import forms
from schedules.models import Schedule

class ScheduleForm(forms.ModelForm):
        
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'schedule_day': forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_time': forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_course': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_class': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }
