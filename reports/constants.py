from django.utils.translation import gettext_lazy as _


WEEKDAYS = {
    0: _("Senin"),
    1: _("Selasa"),
    2: _("Rabu"),
    3: _("Kamis"),
    4: _("Jumat"),
    5: _("Sabtu"),
    6: _("Ahad"),
}

STATUS_CHOICES = (
    (None, "----Pilih Status----"),
    ("Hadir", _("Hadir")),
    ("Izin", _("Izin")),
    ("Sakit", _("Sakit")),
    ("Tanpa Keterangan", _("Tanpa Keterangan")),
)