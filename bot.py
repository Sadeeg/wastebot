import os
import sqlite3
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests
from icalendar import Calendar

ICS_URL = os.getenv('ICS_URL')
REMINDER_HOUR = int(os.getenv('REMINDER_HOUR', '18'))
TIMEZONE = ZoneInfo(os.getenv('TIMEZONE', 'Europe/Berlin'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

DB_PATH = '/data/wastebot.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS sent(date TEXT PRIMARY KEY)')
    conn.commit()
    return conn

def fetch_ics():
    r = requests.get(ICS_URL, timeout=15)
    r.raise_for_status()
    return Calendar.from_ical(r.content)

def get_tomorrow_events(cal):
    today = datetime.now(TIMEZONE).date()
    tomorrow = today + timedelta(days=1)
    events = []
    for comp in cal.walk('VEVENT'):
        dt = comp.get('DTSTART').dt
        if isinstance(dt, datetime):
            dt = dt.date()
        if dt == tomorrow:
            summary = str(comp.get('SUMMARY'))
            events.append(summary)
    return events

def send_telegram(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text}, timeout=15)

def main():
    if not all([ICS_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
        print('Missing env vars')
        return
    cal = fetch_ics()
    events = get_tomorrow_events(cal)
    if not events:
        print('No events tomorrow')
        return
    today_str = datetime.now(TIMEZONE).date().isoformat()
    conn = init_db()
    cur = conn.cursor()
    cur.execute('SELECT 1 FROM sent WHERE date=?', (today_str,))
    if cur.fetchone():
        print('Already sent today')
        return
    msg = f'🗑️ Müll-Erinnerung für morgen, {(datetime.now(TIMEZONE).date()+timedelta(days=1)).strftime("%d.%m.%Y")}\n'
    for e in events:
        msg += f'• {e}\n'
    msg += 'Tonnen bitte heute Abend rausstellen.'
    send_telegram(msg)
    cur.execute('INSERT INTO sent(date) VALUES(?)', (today_str,))
    conn.commit()

if __name__ == '__main__':
    main()
