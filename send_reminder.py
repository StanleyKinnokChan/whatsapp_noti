import os
import sys
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

def send_reminder():
    instance_id = os.environ.get("GREEN_API_INSTANCE_ID")
    api_token = os.environ.get("GREEN_API_TOKEN")
    group_chat_id = os.environ.get("WHATSAPP_GROUP_CHAT_ID")
    message = os.environ.get("REMINDER_MESSAGE", "This is your scheduled reminder!")

    missing = [k for k, v in {
        "GREEN_API_INSTANCE_ID": instance_id,
        "GREEN_API_TOKEN": api_token,
        "WHATSAPP_GROUP_CHAT_ID": group_chat_id,
    }.items() if not v]

    if missing:
        print(f"[ERROR] Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{api_token}"
    payload = {
        "chatId": group_chat_id,
        "message": message,
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] Sending reminder to group {group_chat_id}...")

    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        print(f"[{timestamp}] SUCCESS — Status: {response.status_code} | Response: {response.text}")
    except requests.exceptions.HTTPError as e:
        print(f"[{timestamp}] HTTP ERROR — {e} | Response: {response.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] REQUEST ERROR — {e}")
        sys.exit(1)


if __name__ == "__main__":
    send_reminder()
