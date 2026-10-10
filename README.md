# wastebot

Telegram Müll-Erinnerung 1 Tag vorher für Ihre Gemeinde

## Umgebungsvariablen
ICS_URL
REMINDER_HOUR
TIMEZONE
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

## Nutzung
docker compose up -d
Cron läuft automatisch täglich um REMINDER_HOUR Uhr in TIMEZONE.

## Beispiel .env
ICS_URL=webcal://example.com/Gemeinde/Landkreis/Ihre-Gemeinde/ics?RESTMUELL=true&BIO=true&YELLOW_SACK=true&PAPER=true
REMINDER_HOUR=18
TIMEZONE=Europe/Berlin
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=-100xxxxxx
