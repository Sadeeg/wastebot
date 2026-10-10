#!/bin/sh
set -e
HOUR=${REMINDER_HOUR:-18}
CRON_EXPR="0 $HOUR * * *"
echo "$CRON_EXPR python /app/bot.py >> /var/log/cron.log 2>&1" | crontab -
cron -f
