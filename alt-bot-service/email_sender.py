import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel
from typing import List


class EmailContent(BaseModel):
    content: List[str]


def get_content_as_MIMEText(content: EmailContent):
    return map(lambda x: MIMEText(x + "\n", "plain"), content.content)


def send_email(content: EmailContent):
    # The mail addresses and password
    sender_address = 'tdallas@itba.edu.ar'
    sender_pass = 'iuhwwzbebfmxezhx'
    receivers = ['tdallas@itba.edu.ar']
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receivers)
    message['Subject'] = '[Mail de prueba] Nuevos pares listados en binance'  # The subject line
    for pair in get_content_as_MIMEText(content):
        message.attach(pair)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, ", ".join(receivers), text)
    session.quit()
