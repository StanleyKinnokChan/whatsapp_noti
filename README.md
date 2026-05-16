# WhatsApp Group Reminder

Sends a scheduled WhatsApp message to a group using [Green API](https://green-api.com) and GitHub Actions. Runs entirely in the cloud — no server or open computer needed.

## How it works

1. GitHub Actions triggers the script on a cron schedule
2. `send_reminder.py` calls the Green API to send a message to your WhatsApp group
3. Logs are available in the GitHub Actions run history

## Project structure

```
whatsapp_noti/
├── .github/
│   └── workflows/
│       └── send_reminder.yml   # Schedule + CI definition
├── send_reminder.py            # Main script
├── requirements.txt
└── .env.example                # Template for local development
```

## Setup

### 1. Green API account

1. Sign up at [green-api.com](https://green-api.com) (free)
2. Create an instance — note the **Instance ID** and **API Token**
3. Scan the QR code with the WhatsApp account that will send messages (done once)

### 2. Find your group chat ID

Call this URL in your browser (replace with your credentials):

```
https://api.green-api.com/waInstance{INSTANCE_ID}/getChats/{API_TOKEN}
```

Find your group in the list — the `id` looks like `120363XXXXXXXXXX@g.us`.

### 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/whatsapp_noti.git
git push -u origin main
```

### 4. Add GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret | Value |
|---|---|
| `GREEN_API_INSTANCE_ID` | Your instance ID |
| `GREEN_API_TOKEN` | Your API token |
| `WHATSAPP_GROUP_CHAT_ID` | e.g. `120363XXXXXXXXXX@g.us` |
| `REMINDER_MESSAGE` | The message text to send |

### 5. Test manually

Go to **Actions** → **Send WhatsApp Reminder** → **Run workflow**. Check the logs for `SUCCESS`.

### 6. Adjust the schedule

Edit the cron expression in `.github/workflows/send_reminder.yml`:

```yaml
- cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC
```

GitHub Actions uses **UTC**. Use [crontab.guru](https://crontab.guru) to build your schedule.

> UTC+8 example: to send at 9:00 AM local time, use `0 1 * * 1` (1:00 AM UTC = 9:00 AM UTC+8)

## Local development

```bash
cp .env.example .env
# Fill in your credentials in .env
pip install -r requirements.txt
python send_reminder.py
```
