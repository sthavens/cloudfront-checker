import json
import sys
import requests
import time
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

secrets = {}
kwargs = {}
WAIT_TIME = 24 * 60 * 60 #seconds and checks before request
POLLING_RATE = 30 #seconds from end of last get request til next poll. Decrease for lower throughput or higher latency connections

def send_sms(to_phone_number):
    twilio_client = Client(secrets["TWILIO_ACCOUNT_SID"], secrets["TWILIO_AUTH_TOKEN"])
    twilio_from = secrets["TWILIO_NUMBER"]
    twilio_client.messages.create(body="Your Cloudfront CDN page is ready.", from_=f"{twilio_from}", to=f"{to_phone_number}")

def send_email(to_email):
    try:
        server = smtplib.SMTP(secrets["SMTP_SERVER"], 587)
        server.ehlo
        server.starttls()
        server.login(secrets["EMAIL_ACCOUNT"], secrets["EMAIL_PASSWORD"])
        sent_from = secrets["EMAIL_ACCOUNT"]
        subject = "Cloudfront CDN"
        body = "Your Cloudfront CDN page is ready"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sent_from
        msg['To'] = to_email
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(f"Email send failed: {e}")
        raise


def get_header(url):
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < WAIT_TIME:
        text = requests.get(url)
        if "type" in kwargs:
            image_type = kwargs["type"]
        else:
            image_type = "image/jpeg"
        if text.headers['Content-Type'] == image_type:
            if (secrets["TWILIO_ACCOUNT_SID"] and secrets["TWILIO_AUTH_TOKEN"]) and "phone" in kwargs:
                phone = kwargs["phone"]
                print(f"Sent Text to {phone}")
                send_sms(phone)
            if (secrets["EMAIL_ACCOUNT"] and secrets["EMAIL_PASSWORD"] and secrets["SMTP_SERVER"]) and "email" in kwargs:
                email = kwargs["email"]
                send_email(email)
                print(f"Sent Email to {email}")
            print("Done")
            break
        time.sleep(POLLING_RATE)
    if time.perf_counter() - start_time >= WAIT_TIME:
        print(f"Timed Out after {time.perf_counter() - start_time} seconds")
    
def main():
    args = sys.argv
    if len(args) < 2:
        print("The url must be provded as a command line argument")
        return
    url = args[1]
    if len(args) > 2:
        args = args[2:]
        for arg in args:
            kwargs[arg.split('=')[0]] = arg.split('=')[1]
    get_header(url)
    

if __name__ == '__main__':
    with open("secrets.json", "r") as f:
        file_data= f.read()    
    secrets = json.loads(file_data)
    main()