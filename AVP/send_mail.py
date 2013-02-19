import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

send_from = 'jenko.kov@gmail.com'


def send_mail(send_to, subject, text, file):

    msg = MIMEMultipart()
    msg['From'] = 'ITLand Root'
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(file, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('jenko.kov', 'efi42dekut')
    server.sendmail(send_from, send_to, msg.as_string())
    server.quit()

    #server=smtplib.SMTP('172.16.10.254:25')
    #server.sendmail(send_from, send_to, msg.as_string())
    #server.quit()