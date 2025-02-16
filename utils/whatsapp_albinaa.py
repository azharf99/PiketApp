from typing import Any
import requests
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
token = os.getenv("WA_AIS_TOKEN")
admin_phone = os.getenv("ADMIN_PHONE")
sender_albinaa_phone = os.getenv("SENDER_ALBINAA_PHONE")

def send_whatsapp_action(user: Any = "Anda", phone: str | None = admin_phone, action: str = "", messages: str = "", type: str = "", slug: str = "") -> requests.Response | None:        
    message = f'''*[NOTIFIKASI PIKET]*
{user} berhasil {action} {messages}.
Detail:
https://piket.albinaa.sch.id/{type}{slug}
'''
    url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=62{phone[1:] if phone.startswith('0') and phone != '0' else admin_phone[1:]}&pesan={message}"
    url_helmi = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=6285860256426&pesan={messages}"

    try:
        data = None
        data = requests.get(url, timeout=5)
        if not settings.DEBUG:
            data = requests.get(url_helmi, timeout=5)
        return data
    except:
        return None


def send_whatsapp_report(messages: str = "") -> requests.Response | None:        
    url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=6285701570100&pesan={messages}"
    if not settings.DEBUG:
        url_helmi = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=6285860256426&pesan={messages}"
        url_ghozali = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=62895385277028&pesan={messages}"

    try:
        data = requests.get(url, timeout=5)
        if not settings.DEBUG:
            data = requests.get(url_helmi, timeout=5)
            data = requests.get(url_ghozali, timeout=5)
        return data
    except:
        return None