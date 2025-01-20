from django import forms
from courses.models import Course
from schedules.models import ReporterSchedule, Schedule

class ScheduleForm(forms.ModelForm):
        
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'schedule_day': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_time': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_course': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_class': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'time_start': forms.TimeInput(attrs={"type":"time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'time_end': forms.TimeInput(attrs={"type":"time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize related queries
        self.fields['schedule_course'].queryset = Course.objects.select_related('teacher')



class ReporterScheduleForm(forms.ModelForm):
        
    class Meta:
        model = ReporterSchedule
        fields = '__all__'
        widgets = {
            'schedule_day': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule_time': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'reporter': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'time_start': forms.TimeInput(attrs={"type":"time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'time_end': forms.TimeInput(attrs={"type":"time", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }