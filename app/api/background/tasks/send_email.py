import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email_to_users(emails=[]):

    try:
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.environ.get("EMAIL_USER_NAME")
        sender_password = os.environ.get("EMAIL_USER_PASSWORD")

        # Set up the email message
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["Subject"] = "Test Email from FastAPI"

        # Add the message body
        body = "This is a test email sent from FastAPI."
        message.attach(MIMEText(body, "plain"))

        for recipient_email in emails:

            # Connect to the SMTP server and authenticate
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)

                # Send the email
                text = message.as_string()
                server.sendmail(sender_email, recipient_email, text)
                print("🚀")

    except Exception as e:
        print(e)
