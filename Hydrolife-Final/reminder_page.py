
import schedule
import time
from threading import Thread
from plyer import notification

def reminder_start(interval_minutes):
    def remind():
        notification.notify(
            title="💧 Water Reminder",
            motivation="Time to drink water!",
            timeout=5
        )

    schedule.every(interval_minutes).minutes.do(remind)

    def scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    
    Thread(target=scheduler, daemon=True).start()
