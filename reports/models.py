from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from schedules.models import Schedule
from datetime import datetime
from utils.constants import STATUS_CHOICES, WEEKDAYS


class Report(models.Model):
    report_date = models.DateField(_("Tanggal"))
    report_day = models.CharField(_("Hari"), max_length=20, blank=True, help_text=_("Opsional. Auto-generated"))
    duty = models.TextField(_("Tugas"), max_length=250, blank=True, null=True, help_text=_("Opsional. Jika ada"))
    notes = models.TextField(_("Keterangan"), max_length=250, blank=True, null=True, help_text=_("Opsional. Jika ada"))
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, verbose_name=_("Jadwal"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[1][0])
    subtitute_teacher = models.ForeignKey(User, related_name="subtitute_teacher", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Guru Pengganti"))
    reporter = models.ForeignKey(User, related_name="reporter", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Petugas Piket"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def report_day(self):
        return WEEKDAYS.get(self.report_date.weekday(), "Error")

    def __str__(self) -> str:
        return F"{self.report_date.strftime('%Y-%m-%d')} | {self.status} | {self.schedule}"
    

    def get_absolute_url(self) -> str:
        return reverse("report-list")
    

    class Meta:
        ordering = ["-report_date", "schedule__schedule_class", "schedule__schedule_time"]
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        db_table = "reports"
        indexes = [
            models.Index(fields=["report_date"]),
        ]
