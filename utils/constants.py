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

CLASS_CATEGORY_CHOICES = (
    (None, "----Pilih Kategori Kelas----"),
    ("Putra", _("Putra")),
    ("Putri", _("Putri")),
)

COURSE_CATEGORY_CHOICES = (
    (None, "----Pilih Kategori----"),
    ("Syar'i", _("Syar'i")),
    ("Ashri", _("Ashri")),
)

SCHEDULE_WEEKDAYS = (
    ("0", _("Senin")),
    ("1", _("Selasa")),
    ("2", _("Rabu")),
    ("3", _("Kamis")),
    ("4", _("Jumat")),
    ("5", _("Sabtu")),
    ("6", _("Ahad")),
)

SCHEDULE_TIME = (
    ("1", _("Jam ke-1")),
    ("2", _("Jam ke-2")),
    ("3", _("Jam ke-3")),
    ("4", _("Jam ke-4")),
    ("5", _("Jam ke-5")),
    ("6", _("Jam ke-6")),
    ("7", _("Jam ke-7")),
    ("8", _("Jam ke-8")),
    ("9", _("Jam ke-9")),
)