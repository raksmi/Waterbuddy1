
import schedule
import time
from threading import Thread
from plyer import notification

def start_reminder(interval_minutes):
    def remind():
        notification.notify(
            title="💧 Water Reminder",
            message="Time to drink water!",
            timeout=5
        )

    schedule.every(interval_minutes).minutes.do(remind)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    
    Thread(target=run_scheduler, daemon=True).start()

