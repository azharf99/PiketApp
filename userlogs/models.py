from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.
class UserLog(models.Model):
    user = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=200)
    app = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.action_flag} | {self.app} | {self.message}"

    def get_absolute_url(self):
        return reverse("userlog-list")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Userlog")
        verbose_name_plural = _("Userlogs")
        db_table = "userlogs"
        indexes = [
            models.Index(fields=["id",]),
        ]
