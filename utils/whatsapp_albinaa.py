import json
from typing import Any
import requests
import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
token_wablas = os.getenv("WABLAS_TOKEN")
admin_phone = os.getenv("ADMIN_PHONE")
piket_group_phone = os.getenv("PIKET_GROUP_PHONE")
sender_albinaa_phone = os.getenv("SENDER_ALBINAA_PHONE")

def send_whatsapp_action(user: Any = "Anda", phone: str | None = admin_phone, action: str = "", messages: str = "", type: str = "", slug: str = "") -> requests.Response | None:        
    message = f'''*[NOTIFIKASI PIKET]*
{user} berhasil {action} {messages}.
Detail:
https://piket.albinaa.sch.id/{type}{slug}
'''
    url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=62{phone[1:] if phone.startswith('0') and phone != '0' else admin_phone[1:]}&pesan={message}"
    try:
        data = requests.get(url, timeout=5)
        return data
    except:
        return None

def send_whatsapp_group(messages: str = "") -> requests.Response | None:        
    url_wablas = "https://jogja.wablas.com/api/v2/send-message"
    payload = {
        "data": [
            {
                'phone': piket_group_phone,
                'message': messages,
                'isGroup': 'true'
            },
            # {
            #     'phone': '120363322382144100',
            #     'message': messages,
            #     'isGroup': 'true'
            # },
            {
                'phone': '085701570100',
                'message': messages,
            },
            {
                'phone': '085860256426',
                'message': messages,
            },
            {
                'phone': '085710114880', 
                'message': messages,
            },
        ]
    }

    headers = {
        "Authorization": token_wablas,
        "Content-Type": "application/json"
    }
    try:
        if not settings.DEBUG:
            data = requests.post(url_wablas, headers=headers, data=json.dumps(payload), verify=False, timeout=5)  # Disables SSL verification)
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def send_whatsapp_report(messages: str = "") -> requests.Response | None:        
    url = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=6285701570100&pesan={messages}"
    if not settings.DEBUG:
        url_helmi = f"https://albinaa.sch.id/wp-content/wa/api.php?sender={sender_albinaa_phone}&no=6285860256426&pesan={messages}"

    try:
        data = requests.get(url, timeout=5)
        if not settings.DEBUG:
            data = requests.get(url_helmi, timeout=5)
        return data
    except:
        return None