import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import PairContent, TradeData


def get_content_as_MIMEText(content: str):
    return MIMEText("Nuevos pares listados: \n" + content, "plain")


def get_content_for_pairs(pairs: [PairContent]):
    mapped = list(map(lambda x: x.pair + " | " + x.date + " UTC\n", pairs))
    return "".join(mapped)


def send_email(pairs: [PairContent]):
    if len(pairs) > 0:
        # The mail addresses and password
        sender_address = 'tdallas@itba.edu.ar'
        sender_pass = 'iuhwwzbebfmxezhx'
        receivers = ['tdallas@itba.edu.ar']
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = ", ".join(receivers)
        message['Subject'] = '[Mail automático] Nuevos pares listados en binance'  # The subject line
        content = get_content_for_pairs(pairs)
        message.attach(get_content_as_MIMEText(content))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receivers, text)
        session.quit()


def send_trade_done_email(tradeData: TradeData):
    pass
