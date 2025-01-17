import requests
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
token = os.getenv("WA_AIS_TOKEN")
admin_phone = os.getenv("ADMIN_PHONE")
sender_ais_phone = os.getenv("SENDER_AIS_PHONE")

def send_whatsapp_action(phone: str | None = admin_phone, action: str = "", messages: str = "", type: str = "", slug: str = "") -> requests.Response | None:        
    message = f'''*[NOTIFIKASI PIKET]*
Anda berhasil {action} {messages}.
Detail:
https://piket.albinaa.sch.id/{type}{slug}
'''
    url = f"https://sent.fafashop.my.id/send-message?api_key={token}&sender={sender_ais_phone}&number={phone}&message={message}"

    try:
        data = requests.get(url, timeout=5)
        return data
    except:
        return None
