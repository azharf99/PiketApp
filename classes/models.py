from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from utils.constants import CLASS_CATEGORY_CHOICES

# Create your models here.
class Class(models.Model):
    class_name = models.CharField(_("Nama Kelas"), max_length=50, unique=True)
    short_class_name = models.CharField(_("Nama Singkat Kelas"), max_length=20)
    category = models.CharField(_("Kode Pelajaran"), max_length=20, choices=CLASS_CATEGORY_CHOICES, default=CLASS_CATEGORY_CHOICES[1][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.short_class_name
    

    def get_absolute_url(self):
        return reverse("class-list")
    

    class Meta:
        ordering = ["class_name"]
        verbose_name = _("Class")
        verbose_name_plural = _("Classes")
        db_table = "classes"
        indexes = [
            models.Index(fields=["id", "class_name"]),
        ]
    


