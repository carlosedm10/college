import base64
import os
import ssl
import sys
import smtplib

from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


PDF_PATH = "/Users/carlosedm10/projects/college/DST/PDF_PRAC3.pdf"

SMTP_SERVER = "smtp.upv.es"
SMTP_PORT = 587

EMAIL_FROM = os.getenv("UPV_USERNAME")
EMAIL_PASS = str(os.getenv("EMAIL_PASS"))
EMAIL_TO = "practica.dst@gmail.com"
EMAIL_SUBJECT = "Prac3"
DNI = str(os.getenv("DNI"))
EMAIL_MESSAGE = f"Mi nombre es: Carlos Eduardo \n Mi DNI es: {DNI}"


def validate_email_custom(email):
    """
    Custom email validation function
    """
    if not validate_email(
        email_address=email,
        check_format=True,
        check_blacklist=True,
        check_dns=False,
        check_smtp=False,
    ):
        print("El email no es valido")
        exit(1)
    else:
        print("El email es valido")


validate_email_custom(EMAIL_TO)
msg = MIMEMultipart("mixed", "frontera")
msg.add_header("From", EMAIL_FROM)
msg.add_header("To", EMAIL_TO)
msg.add_header("Subject", EMAIL_SUBJECT)
text_msg = MIMEText(EMAIL_MESSAGE, "plain", "utf-8")
msg.attach(text_msg)

try:
    file = open(PDF_PATH, "rb")
    document = MIMEApplication(file.read(), "pdf")
    document.add_header(
        "ContentDisposition", 'attachment; filename = "' + PDF_PATH + '"'
    )
    msg.attach(document)
    file.close()
except OSError as e:
    print(e)
    print("OS Error sending mail")
    sys.exit()


try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as mailServer:
        mailServer.set_debuglevel(1)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(EMAIL_FROM, EMAIL_PASS)

        print(f"Mail sent to {EMAIL_TO} from {EMAIL_FROM} with subject {EMAIL_SUBJECT}")
except smtplib.SMTPException as e:
    print(e)
    print("Error sending mail")
    sys.exit()
