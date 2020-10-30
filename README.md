# cloudfront-checker
A tool to monitor when a cloudfront implementation has reached the dns server (no longer redirects to the endpoint)

Please feel free to fork and modify as you wish.

To set up, 

If you wish, create a virtual environment
pip (or pip3) install requirements.txt
python (or python3) cloudfront-checker.py *URL* with optional phone=*phone number with country/region code* and/or email=*email address* type=*file type (default is image/jpeg)*

ex: python3 cloudfront-checker.py xyzpdq.cloudfront.net/ou812.jpg phone=+13105551212 email=test@example.com

You may also wish to modify the default polling rate and the total wait time. These are at the top of the python script. The default is to check every 30 seconds for a maximum of 24 hours (of course, this should exit earlier than that if cloudfront is configured correctly).

Please make yourself a secrets.json file in the following form to enable notification of completion:

{
    "TWILIO_ACCOUNT_SID": "",
    "TWILIO_AUTH_TOKEN": "",
    "TWILIO_NUMBER": "",
    "EMAIL_ACCOUNT": "",
    "EMAIL_PASSWORD": "",
    "SMTP_SERVER": ""
}

Default test is finding a jpeg image, but you can change the file type to whatever file should be found on the cloudfront distribution

If you wish to send yourself a text upon completion, set up a Twilio account (at www.twilio.com) and add the SID and AUTH_TOKEN from the dashboard and set yourself up a phone number at https://www.twilio.com/console/phone-numbers/incoming. Add these to the secrets.json. There is usually a good free trial available.

If you wish to send yourself an email upon completion, put your email account, password, and smtp server in the secrets.json. This functionality was tested using gmail using an "app password" that can be obtained from the security section of a google account.

This was a very quick and simple script that I really do not plan on maintaining but if you want a certain functionality, please throw a request in and I will do my best to add the functionality.

Also, I have not taken the time to learn markdown, so please forgive the poor formatting.