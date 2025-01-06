from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from reports.constants import STATUS_CHOICES, WEEKDAYS
from schedules.models import Schedule


class Report(models.Model):
    report_date = models.DateField(_("Tanggal"), default=timezone.now)
    report_day = models.CharField(_("Hari"), max_length=20, blank=True, help_text=_("Opsional. Auto-generated"))
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, verbose_name=_("Jadwal"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    subtitute_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Guru Pengganti"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def report_day(self):
        return WEEKDAYS.get(self.report_date.weekday(), "Error")

    def __str__(self) -> str:
        return F"{self.report_date.strftime('%Y-%m-%d')} | {self.status} | {self.schedule}"
    

    def get_absolute_url(self) -> str:
        return reverse("schedule-list")
    

    class Meta:
        ordering = ["report_date"]
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        db_table = "reports"
        indexes = [
            models.Index(fields=["report_date"]),
        ]
