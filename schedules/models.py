from classes.models import Class
from courses.models import Course
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from utils.constants import SCHEDULE_WEEKDAYS, SCHEDULE_TIME
from datetime import time
# Create your models here.

class Schedule(models.Model):
    schedule_day = models.CharField(_("Hari"), max_length=10, blank=True, choices=SCHEDULE_WEEKDAYS)
    schedule_time = models.CharField(_("Jam Ke-"), max_length=20, choices=SCHEDULE_TIME)
    schedule_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name=_("Pelajaran"))
    schedule_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, verbose_name=_("Kelas"))
    time_start = models.TimeField(_("Waktu Mulai"), default=time(7, 0, 0, 0))
    time_end = models.TimeField(_("Waktu Akhir"), default=time(7, 0, 0, 0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return F"{self.get_schedule_day_display()} | Jam ke-{self.schedule_time} | {self.schedule_class} | {self.schedule_course}"
    

    def get_absolute_url(self) -> str:
        return reverse("schedule-list")
    

    class Meta:
        ordering = ["-schedule_day", "schedule_class", "schedule_time"]
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        db_table = "schedules"
        indexes = [
            models.Index(fields=["schedule_day"]),
        ]
    

