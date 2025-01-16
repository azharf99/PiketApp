from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField, ModelForm
from reports.models import Report
from schedules.models import Schedule
from utils.constants import SCHEDULE_TIME
from utils.validate_datetime import validate_date, validate_time, get_day

class ReportForm(forms.ModelForm):
        
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'report_date': forms.DateInput(attrs={"type":"date", "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'report_day': forms.TextInput(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'schedule': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'status': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'subtitute_teacher': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'reporter': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize related queries
        self.fields['schedule'].queryset = Schedule.objects.select_related("schedule_course", "schedule_course__teacher","schedule_class")


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name if obj.first_name else obj.username
    
class ReportFormV2(forms.ModelForm):
    subtitute_teacher = UserModelChoiceField(
        required=False,
        queryset=User.objects.all().order_by('first_name'),
        widget=forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"})
        )
    reporter = UserModelChoiceField(
        required=False,
        queryset=User.objects.all().order_by('first_name'),
        widget=forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"})
        )
        
    class Meta:
        model = Report
        fields = ['status', 'subtitute_teacher', 'reporter']
        widgets = {
            'status': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'subtitute_teacher': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
            'reporter': forms.Select(attrs={"class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg"}),
        }
        

class QuickReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Extract additional parameters from kwargs
        report_date = kwargs.pop('report_date', None)
        schedule_time = kwargs.pop('schedule_time', None)

        valid_report_date = validate_date(report_date)
        valid_schedule_time = validate_time(schedule_time)

        # Call the superclass initializer
        super().__init__(*args, **kwargs)
        
        # Dynamically set field attributes based on provided parameters
        if valid_report_date:
            self.fields['report_date'].widget.attrs['value'] = report_date
        else: 
            self.fields['report_date'].widget.attrs['value'] = datetime.now().date()
        if valid_schedule_time:
            self.fields['schedule_time'].initial = schedule_time

    # Define fields at the class level
    report_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg",
                "type": "date",
            }
        ),
    )
    schedule_time = forms.ChoiceField(
        choices=SCHEDULE_TIME,
        required=True,
        widget=forms.Select(
            attrs={
                "class": "rounded-md text-black px-2 py-1 border-2 border-blue-500 dark:border-none shadow-lg",
            }
        ),
    )