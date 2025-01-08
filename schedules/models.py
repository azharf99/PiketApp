from classes.models import Class
from courses.models import Course
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from schedules.constants import WEEKDAYS, SCHEDULE_TIME

# Create your models here.

class Schedule(models.Model):
    schedule_day = models.CharField(_("Hari"), max_length=10, blank=True, choices=WEEKDAYS)
    schedule_time = models.CharField(_("Waktu"), max_length=20, choices=SCHEDULE_TIME)
    schedule_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name=_("Pelajaran"))
    schedule_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, verbose_name=_("Kelas"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return F"{self.schedule_day} | Jam ke-{self.schedule_time} | {self.schedule_class} | {self.schedule_course}"
    

    def get_absolute_url(self) -> str:
        return reverse("schedule-list")
    

    class Meta:
        ordering = ["-schedule_day", "schedule_class"]
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        db_table = "schedules"
        indexes = [
            models.Index(fields=["schedule_day"]),
        ]
    

